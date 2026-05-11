#!/usr/bin/env python3
import asyncio
import json
import logging
import random
import time
from typing import Dict, List, Any
import pickle
import os

# msgpack is optional
try:
    import msgpack  # type: ignore
except Exception:  # pragma: no cover
    msgpack = None

# Import judge classes
from llm_client import LLMJudge, LLMJudgeConfig, RewardModelJudge

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("AsyncInferenceServer")

# -----------------------------
# Wire format helpers
# -----------------------------
def decode_payload(data: bytes) -> tuple[list[dict], str]:
    """
    Try to decode payload in order: pickle, msgpack.
    Returns (obj, format) where format in {"pickle","msgpack"}.
    Raises ValueError if all decoding attempts fail.
    """

    # 1) pickle
    try:
        obj = pickle.loads(data)
        if isinstance(obj, list):
            return obj, "pickle"
    except Exception:
        pass

    # 2) msgpack (optional)
    if msgpack is not None:
        try:
            obj = msgpack.unpackb(data, raw=False)
            if isinstance(obj, list):
                return obj, "msgpack"
        except Exception:
            pass

    raise ValueError("Unsupported or corrupted payload: cannot decode as pickle/msgpack list")


def encode_payload(fmt: str, obj: Any) -> bytes:
    """
    Encode obj according to fmt.
    """
    if fmt == "json":
        return json.dumps(obj).encode('utf-8')
    if fmt == "pickle":
        return pickle.dumps(obj, protocol=pickle.HIGHEST_PROTOCOL)
    if fmt == "msgpack":
        if msgpack is None:
            raise ValueError("msgpack not available on server")
        return msgpack.packb(obj, use_bin_type=True)
    # default to json if unknown
    return json.dumps(obj).encode('utf-8')

class AsyncInferenceServer:
    """Async inference server that processes client requests and returns results."""
    
    def __init__(self, host: str = '127.0.0.1', port: int = 8133):
        self.host = host
        self.port = port
        self.server = None
        
        mode = os.getenv("JUDGE_MODE", "llm")  # New environment variable
        if mode == "reward_model":
            self.llm_judge = RewardModelJudge()
        else:
            config = LLMJudgeConfig(
                api_key="123",
                base_url="http://0.0.0.0:8112/v1",
                temperature=0.3,
                max_tokens=48
            )
            self.llm_judge = LLMJudge(config)
    
    async def _execute_sync_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute synchronous tasks using LLMJudge for inference.
        
        Args:
            task_data: Dictionary containing task info
        
        Returns:
            Updated task dictionary containing the result
        """
        # Record start time
        start_time = time.time()
        
        # Get prompt
        prompt = task_data.get('prompt', '')
        if not prompt:
            logger.debug("prompt is empty")

        # Use LLMJudge for prediction
        try:
            # Use asyncio.to_thread to convert sync method to async execution
            response = await asyncio.to_thread(self.llm_judge.predict, prompt)
        except Exception as e:
            logger.error(f"LLMJudge prediction error: {e}")
            response = f"Error: {str(e)}"
        
        # Calculate total time elapsed
        time_cost = time.time() - start_time
        
        # Update task data
        result = task_data.copy()
        result["answer"] = response
        
        logger.info(f"Processed task ID: {task_data.get('id', 'unknown')}, cost: {time_cost:.4f}s")
        
        return result
    
    async def _process_batch(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Process a batch of tasks.
        
        Args:
            tasks: List of tasks
            
        Returns:
            List of results
        """
        logger.info(f"Received batch request with {len(tasks)} tasks")
        
        # Create async task list
        async_tasks = [self._execute_sync_task(task) for task in tasks]
        
        # Execute all tasks concurrently
        results = await asyncio.gather(*async_tasks)
        
        logger.info(f"Batch processing complete, returned {len(results)} results")
        return results
    
    async def _handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        """
        Handle client connection.
        
        Args:
            reader: Stream for reading client data
            writer: Stream for writing data to the client
        """
        peer_name = writer.get_extra_info('peername')
        logger.info(f"Client connection: {peer_name}")
        
        try:
            # Read data length (4 bytes)
            data_len_bytes = await reader.read(4)
            if not data_len_bytes:
                logger.warning(f"Client {peer_name} sent empty data")
                self._send_error_response(writer, "Empty data received")
                return
                
            data_len = int.from_bytes(data_len_bytes, byteorder='big')
            logger.info(f"Preparing to receive data, length: {data_len} bytes")
            
            # Read data - use chunked reading to ensure complete reception
            chunks = []
            bytes_read = 0
            
            while bytes_read < data_len:
                # Read up to 64KB per chunk
                chunk = await reader.read(min(65536, data_len - bytes_read))
                if not chunk:
                    # Connection closed or read error
                    break
                    
                chunks.append(chunk)
                bytes_read += len(chunk)
                
            # Combine all data chunks
            data = b''.join(chunks)
            
            if not data or bytes_read < data_len:
                logger.warning(f"Client {peer_name} data reception incomplete: expected {data_len} bytes, got {bytes_read} bytes")
                self._send_error_response(writer, f"Incomplete data received: expected {data_len} bytes, got {bytes_read} bytes")
                return
            
            # Decode request data (supports JSON / pickle / msgpack)
            try:
                tasks, req_fmt = decode_payload(data)
                logger.info(f"Request payload format: {req_fmt}")
            except Exception as e:
                error_msg = f"Error decoding data: {e}"
                logger.error(error_msg)
                self._send_error_response(writer, error_msg, format_hint="json")
                return
                
            # Handle tasks
            results = await self._process_batch(tasks)
            
            # Encode results (return in the same format as request)
            try:
                result_data = encode_payload(req_fmt, results)
            except Exception as e:
                logger.error(f"Failed to encode in request format, falling back to JSON: {e}")
                result_data = encode_payload("json", results)
            
            # Send result length and content
            writer.write(len(result_data).to_bytes(4, byteorder='big'))
            writer.write(result_data)
            await writer.drain()
            
            logger.info(f"Results sent to client {peer_name}")
            
        except Exception as e:
            error_msg = f"Error handling client request: {e}"
            logger.error(error_msg, exc_info=True)
            self._send_error_response(writer, error_msg)
        finally:
            # Close connection
            writer.close()
            await writer.wait_closed()
            logger.info(f"Client connection closed: {peer_name}")
            
    def _send_error_response(self, writer: asyncio.StreamWriter, error_message: str, format_hint: str = "json"):
        """
        Send error response to client.
        
        Args:
            writer: Stream for writing data to client
            error_message: Error message
        """
        try:
            # Create error response, maintaining consistency with normal format
            error_response = [{
                "id": "error",
                "error": True,
                "error_message": error_message,
                "answer": f"Error: {error_message}"
            }]
            
            # Encode error response
            try:
                response_data = encode_payload(format_hint, error_response)
            except Exception:
                response_data = encode_payload("json", error_response)
            
            # Send error response length and content
            writer.write(len(response_data).to_bytes(4, byteorder='big'))
            writer.write(response_data)
            writer.drain()
            
            logger.info(f"Error response sent: {error_message}")
        except Exception as e:
            logger.error(f"Error sending error response: {e}", exc_info=True)
    
    async def start(self):
        """Start server"""
        self.server = await asyncio.start_server(
            self._handle_client, self.host, self.port
        )
        
        addr = self.server.sockets[0].getsockname()
        logger.info(f'Server started at {addr}')
        
        async with self.server:
            await self.server.serve_forever()
    
    def run(self):
        """Run server (blocking)"""
        try:
            asyncio.run(self.start())
        except KeyboardInterrupt:
            logger.info("Server stopped")

if __name__ == "__main__":
    # Allow host/port override via environment variables
    host = os.environ.get("ASYNC_SERVER_HOST", "127.0.0.1")
    try:
        port = int(os.environ.get("ASYNC_SERVER_PORT", "8133"))
    except Exception:
        port = 8133
    server = AsyncInferenceServer(host=host, port=port)
    logger.info(f"Starting async inference server... {host}:{port}")
    server.run()