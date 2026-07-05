#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sync Client - Uses asynchronous communication internally but provides a synchronous interface.
"""

import asyncio
import json
import logging
import time
import uuid
from typing import Dict, List, Any
import os
import pickle

# msgpack is optional
try:
    import msgpack  # type: ignore
except Exception:
    msgpack = None

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("SyncInferenceClient")

# -----------------------------
# Wire format helpers (client)
# -----------------------------
def _get_wire_format() -> str:
    fmt = os.environ.get("ASYNC_WIRE_FORMAT", "pickle").lower()
    if fmt not in {"pickle", "json", "msgpack"}:
        fmt = "pickle"
    if fmt == "msgpack" and msgpack is None:
        fmt = "json"
    return fmt


def _encode(fmt: str, obj: Any) -> bytes:
    if fmt == "pickle":
        return pickle.dumps(obj, protocol=pickle.HIGHEST_PROTOCOL)
    if fmt == "msgpack":
        if msgpack is None:
            raise ValueError("msgpack not available")
        return msgpack.packb(obj, use_bin_type=True)
    return json.dumps(obj).encode('utf-8')


def _try_decode_with(fmt: str, data: bytes) -> Any:
    try:
        if fmt == "pickle":
            return pickle.loads(data)
        if fmt == "msgpack" and msgpack is not None:
            return msgpack.unpackb(data, raw=False)
        if fmt == "json":
            return json.loads(data.decode('utf-8'))
    except Exception:
        pass
    raise ValueError("decode failed")


def _decode_auto(preferred_fmt: str, data: bytes) -> Any:
    try:
        return _try_decode_with(preferred_fmt, data)
    except Exception:
        pass
    for alt in ("pickle", "msgpack", "json"):
        if alt == preferred_fmt:
            continue
        try:
            return _try_decode_with(alt, data)
        except Exception:
            continue
    return json.loads(data.decode('utf-8', errors='replace'))

class SyncInferenceClient:
    """
    Sync Inference Client - Internal async communication with a synchronous API.
    """
    
    def __init__(self, host: str = '127.0.0.1', port: int = 8133):
        self.host = host
        self.port = port
        print(f"DEBUG: Real Training Client connecting to {self.host}:{self.port}")
    
    def _run_async(self, coro):
        """
        Runs an async coroutine and waits for the result.
        
        Args:
            coro: Asynchronous coroutine.
            
        Returns:
            The result of the coroutine.
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(coro)
        finally:
            loop.close()
    
    async def _send_batch_async(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Sends a batch of tasks to the server and waits for the results.
        
        Args:
            tasks: List of tasks.
            
        Returns:
            List of results processed by the server.
        """
        try:
            logger.info(f"Connecting to server {self.host}:{self.port}")
            reader, writer = await asyncio.open_connection(self.host, self.port)
            
            # Prepare data (defaults to pickle, can be overridden by ASYNC_WIRE_FORMAT)
            wire_fmt = _get_wire_format()
            data = _encode(wire_fmt, tasks)
            
            # Send data length and content
            writer.write(len(data).to_bytes(4, byteorder='big'))
            writer.write(data)
            await writer.drain()
            
            logger.info(f"Sent {len(tasks)} tasks to server")
            
            # Read response length
            resp_len_bytes = await reader.read(4)
            if not resp_len_bytes:
                raise ConnectionError("Server closed the connection")
            resp_len = int.from_bytes(resp_len_bytes, byteorder='big')
            
            # Read response data (chunked to ensure complete read)
            chunks = []
            bytes_read = 0
            while bytes_read < resp_len:
                chunk = await reader.read(min(65536, resp_len - bytes_read))
                if not chunk:
                    break
                chunks.append(chunk)
                bytes_read += len(chunk)
            resp_data = b"".join(chunks)
            if not resp_data or bytes_read < resp_len:
                raise ConnectionError(f"Incomplete response: expected {resp_len} bytes, got {bytes_read} bytes")
            
            # Parse response (decode using the same or compatible format)
            results = _decode_auto(wire_fmt, resp_data)
            
            logger.info(f"Received server response, total {len(results)} results")
            
            # Close connection
            writer.close()
            await writer.wait_closed()
            
            return results
            
        except Exception as e:
            logger.error(f"Error communicating with server: {e}", exc_info=True)
            raise
    
    def predict(self, prompt: str) -> str:
        """
        Sends a single prompt and retrieves the result.
        
        Args:
            prompt: Prompt text.
            
        Returns:
            Generated text.
        """
        # Check if prompt contains special characters
        try:
            # Try to convert to JSON to check for valid characters
            json.dumps({"prompt": prompt})
        except Exception as e:
            logger.warning(f"Prompt contains characters that may cause JSON parsing errors: {e}")
            # Escape special characters
            prompt = prompt.replace("\\", "\\\\").replace("\"", "\\\"").replace("\n", "\\n").replace("\r", "\\r").replace("\t", "\\t")
        
        # Create task with a unique ID
        task_id = f"task-{uuid.uuid4()}"
        task = {
            "id": task_id,
            "prompt": prompt,
            "extra_info": {"timestamp": time.time()}
        }
        
        try:
            # Send request and get results
            results = self._run_async(self._send_batch_async([task]))
            
            # Check for error response
            if len(results) == 1 and results[0].get("error", False):
                error_msg = results[0].get("error_message", "Unknown server error")
                return f"Error: {error_msg}"
            
            # Search for matching ID in results
            for result in results:
                if result.get("id") == task_id:
                    answer = result.get("answer", "")
                    # Extract actual response part if formatted
                    if "Response:" in answer:
                        return answer.split("Response:", 1)[1].strip()
                    return answer
            
            # Handle cases where ID is not found
            if results and len(results) > 0:
                logger.warning(f"No matching task ID found {task_id}, using first result")
                answer = results[0].get("answer", "")
                if "Response:" in answer:
                    return answer.split("Response:", 1)[1].strip()
                return answer
            else:
                return "Error: No response received"
        except Exception as e:
            logger.error(f"Prediction request failed: {e}")
            return f"Error: {str(e)}"
    
    def batch_predict(self, prompts: List[str]) -> List[str]:
        """
        Sends multiple prompts and retrieves results.
        
        Args:
            prompts: List of prompt strings.
            
        Returns:
            List of generated texts, in the same order as input.
        """
        tasks = []
        task_ids = []  # To maintain order
        
        for i, prompt in enumerate(prompts):
            try:
                json.dumps({"prompt": prompt})
            except Exception as e:
                logger.warning(f"Prompt {i+1} contains potentially problematic characters: {e}")
                prompt = prompt.replace("\"", "\\\\").replace('"', '\"').replace('\n', '\\n').replace('\r', '\\r').replace('\t', '\\t')
            
            task_id = f"task-{i+1}-{uuid.uuid4()}"
            tasks.append({
                "id": task_id,
                "prompt": prompt,
                "extra_info": {"timestamp": time.time()}
            })
            task_ids.append(task_id)
        
        try:
            # Send requests and get results
            results = self._run_async(self._send_batch_async(tasks))
            
            # Check for error response
            if len(results) == 1 and results[0].get("error", False):
                error_msg = results[0].get("error_message", "Unknown server error")
                logger.error(f"Server returned error: {error_msg}")
                return [f"Error: {error_msg}"] * len(prompts)
            
            # Map IDs to results
            result_map = {}
            for result in results:
                result_id = result.get("id")
                if result_id:
                    answer = result.get("answer", "Error: No answer received")
                    if "Response:" in answer:
                        result_map[result_id] = answer.split("Response:", 1)[1].strip()
                    else:
                        result_map[result_id] = answer
            
            # Rebuild result list in original order
            answers = []
            for task_id in task_ids:
                if task_id in result_map:
                    answers.append(result_map[task_id])
                else:
                    answers.append(f"Error: No result found for task {task_id}")
            
            if len(answers) != len(prompts):
                logger.warning(f"Result count ({len(answers)}) does not match request count ({len(prompts)})!")
            
            return answers
        except Exception as e:
            logger.error(f"Batch prediction request failed: {e}")
            return [f"Error: {str(e)}"] * len(prompts)

# Test Block
if __name__ == "__main__":
    client = SyncInferenceClient()
    
    # Test single prediction
    print("\nTest single prediction:")
    result = client.predict("Hello, please introduce yourself.")
    print(f"Result: {result[:100]}..." if len(result) > 100 else result)
    
    # Test batch prediction
    print("\nTest batch prediction:")
    test_prompts = [
        "What is 1+1?",
        "What kind of programming language is Python?",
        "Please write a simple greeting."
    ]
    test_results = client.batch_predict(test_prompts)
    for i, res in enumerate(test_results):
        print(f"Result {i+1}: {res[:100]}..." if len(res) > 100 else res)