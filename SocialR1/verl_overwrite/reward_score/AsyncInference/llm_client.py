from typing import Dict, Any, Optional, Union, List, Tuple
from dataclasses import dataclass, field
import re
import json
import time
import os
import pandas as pd
from pathlib import Path
from threading import Lock
from datetime import datetime, timedelta
import asyncio
from client import AsyncInferenceClient
import requests

class RewardModelJudge:
    """Judge based on Reward Model deployed via LLaMA-Factory"""
    def __init__(self, base_url="http://127.0.0.1:8000/v1/score/evaluation", model_path=None):
        self.base_url = os.getenv("OPENAI_API_BASE", base_url)
        self.model_path = model_path or os.getenv("REWARD_MODEL_PATH", "Qwen3_4B_RM")

    def predict(self, prompt: str) -> str:
        payload = {
            "model": self.model_path,
            "messages": [prompt]
        }
        try:
            resp = requests.post(self.base_url, json=payload, timeout=60)
            resp.raise_for_status()
            resp_json = resp.json()
            # Return score as string to maintain consistency with LLMJudge interface
            if "scores" in resp_json:
                return str(resp_json["scores"][0])
            else:
                return str(resp_json)
        except Exception as e:
            return f"Error calling RewardModelJudge: {e}"


@dataclass
class LLMJudgeConfig:
    """Configuration class for LLM Judge"""
    api_key: str = "123"
    base_url: str = "http://0.0.0.0:8112/v1"
    temperature: float = 0.3
    max_tokens: int = 1024
    model_name: Optional[str] = None

class LLMCache:
    _instance = None
    _lock = Lock()
    
    def __new__(cls, cache_file: str = "data/cache_llm.csv"):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance.cache_file = Path(cache_file)
                cls._instance.cache = {}
                cls._instance.last_save_time = time.time()
                cls._instance.save_interval = 600  # 10 minutes in seconds
                cls._instance._load_cache()
            return cls._instance
    
    def _load_cache(self) -> None:
        """Load cache from file if it exists"""
        try:
            if self.cache_file.exists():
                df = pd.read_csv(self.cache_file)
                self.cache = dict(zip(df['prompt'], df['response']))
        except Exception as e:
            print(f"Warning: Failed to load cache: {e}")
    
    def _save_cache(self) -> None:
        """Save cache to file"""
        try:
            self.cache_file.parent.mkdir(parents=True, exist_ok=True)
            df = pd.DataFrame([{"prompt": k, "response": v} for k, v in self.cache.items()])
            df.to_csv(self.cache_file, index=False)
            self.last_save_time = time.time()
        except Exception as e:
            print(f"Warning: Failed to save cache: {e}")
    
    def get(self, prompt: str) -> Tuple[bool, str]:
        """Get response from cache if exists"""
        return prompt in self.cache, self.cache.get(prompt, "")
    
    def set(self, prompt: str, response: str) -> None:
        """Add or update cache entry"""
        self.cache[prompt] = response
        if time.time() - self.last_save_time >= self.save_interval:
            self._save_cache()
    
    def save_if_needed(self) -> None:
        """Save cache to disk if enough time has passed"""
        if time.time() - self.last_save_time >= self.save_interval:
            self._save_cache()


class LLMJudge:
    """Evaluator using LLM to assess model output quality"""
    
    def __init__(self, config: Optional[LLMJudgeConfig] = None):
        """Initialize LLM Judge
        
        Args:
            config: LLMJudgeConfig instance, uses default if None
        """
        self.config = config or LLMJudgeConfig()
        from openai import OpenAI
        api_key = os.getenv("OPENAI_API_KEY", self.config.api_key)
        base_url = os.getenv("OPENAI_API_BASE", self.config.base_url)
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        self.model_name = os.getenv("OPENAI_API_MODEL", self._get_model_name())
        self.cache = LLMCache()
        self.use_cache = os.getenv("LLM_USE_CACHE", "0").lower() in ("1", "true", "yes", "on")
        self.cost_init()

    def cost_init(self):
        """Initialize cost information"""
        self.INPUT_COST_PER_1000_TOKENS = {
            "gpt-4o": 0.0025,
            "gpt-4o_2024-05-13": 0.0025,
            "gpt-4o-mini": 0.00015,
            "o4-mini": 0.00110,
            "o3-mini": 0.00110,
            "o1": 0.015,
            "o1-mini": 0.00110,
            "gpt-3.5-turbo": 0.0005,
            "gpt-35-turbo": 0.0005,
            "o3": 0.0020,
            "gpt-5-chat": 0.00125,
            "gpt-5": 0.00125,
            "gpt-5-mini": 0.00025,
            "gpt-5-nano": 0.00005,
            "gpt-5-chat-latest": 0.00125,
            "gpt-5.1_2025-11-13": 0.00125,
            }
        self.OUTPUT_COST_PER_1000_TOKENS = {
            "gpt-4o": 0.01,
            "gpt-4o_2024-05-13": 0.01,
            "gpt-4o-mini": 0.0006,
            "o4-mini": 0.0044,
            "o3-mini": 0.0044,
            "o1": 0.06,
            "o1-mini": 0.0044,
            "gpt-3.5-turbo": 0.0015,
            "gpt-35-turbo": 0.0015,
            "o3": 0.0080,
            "gpt-5-chat": 0.0100,
            "gpt-5": 0.0100,
            "gpt-5-mini": 0.0020,
            "gpt-5-nano": 0.0004,
            "gpt-5-chat-latest": 0.0100,
            "gpt-5.1_2025-11-13": 0.0100,
        }
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_cost = 0
        self._warned_missing_cost: set = set()
        
    def _get_model_name(self) -> str:
        """Get available model name"""
        if self.config.model_name:
            return self.config.model_name
            
        try:
            models = self.client.models.list()
            for model in models:
                if model.id:
                    return model.id
        except Exception as e:
            print(f"Warning: Failed to get model list: {e}")
        
        return "default_model"

    @staticmethod
    def _extract_xml_content(text: str, tag: str) -> tuple[bool, str]:
        """Extract content from XML tags"""
        if not text or not tag:
            return False, ""
        
        pattern = f"<{tag}>(.*?)</{tag}>"
        match = re.search(pattern, text, re.DOTALL)
        
        if match:
            content = match.group(1).strip()
            if content:
                return True, content
        
        return False, ""

    def predict(self, prompt: str) -> str:
        """Single prediction with cache and retry mechanism"""
        if self.use_cache:
            in_cache, cached_response = self.cache.get(prompt)
            if in_cache:
                return cached_response
            
        max_retries = 5
        retry_delay = 60
        
        for retry_count in range(max_retries):
            try:
                conversation = [{"role": "user", "content": prompt}]
                if any(model in self.model_name for model in ['o1', 'o3', 'o4-mini','gpt-5','gpt-5-mini','gpt-5-nano', 'gpt-5.1_2025-11-13']):
                    response = self.client.chat.completions.create(
                        model=self.model_name,
                        messages=conversation,
                    )
                elif 'qwen3' in self.model_name.lower():
                    response = self.client.chat.completions.create(
                        model=self.model_name,
                        messages=conversation,
                        temperature=self.config.temperature,
                        max_tokens=self.config.max_tokens,
                        extra_body={
                            "chat_template_kwargs": {"enable_thinking": False}
                        },
                    )
                else:
                    response = self.client.chat.completions.create(
                        model=self.model_name,
                        messages=conversation,
                        temperature=self.config.temperature,
                        max_tokens=self.config.max_tokens,
                    )
                
                generated_text = response.choices[0].message.content.strip()
                
                input_tokens = response.usage.prompt_tokens
                output_tokens = response.usage.completion_tokens
                self._update_cost(input_tokens, output_tokens)
                
                if self.use_cache:
                    self.cache.set(prompt, generated_text)
                self.save_cost()
                return generated_text
                
            except Exception as e:
                error_msg = f"Prediction API call failed (Attempt {retry_count + 1}/{max_retries}): {str(e)}"
                print(error_msg)
                
                if retry_count < max_retries - 1:
                    print(f"Waiting {retry_delay} seconds for retry...")
                    import time
                    time.sleep(retry_delay)
                else:
                    print("All retries failed.")
                    return ""
    
    def batch_predict(self, prompts: List[str]) -> List[str]:
        """Batch prediction using AsyncInferenceClient.send_batch"""
        if not prompts:
            return []
            
        results = [None] * len(prompts)
        to_process = []
        to_process_indices = []
        
        if self.use_cache:
            for i, prompt in enumerate(prompts):
                in_cache, cached_response = self.cache.get(prompt)
                if in_cache:
                    results[i] = cached_response
                else:
                    to_process.append(prompt)
                    to_process_indices.append(i)
        else:
            to_process = prompts
            to_process_indices = list(range(len(prompts)))
        
        if not to_process:
            return results
        
        tasks = []
        for i, prompt in enumerate(to_process):
            task_id = str(i)
            tasks.append({
                "id": task_id,
                "prompt": prompt,
                "extra_info": {
                    "model": self.model_name,
                    "temperature": self.config.temperature,
                    "max_tokens": self.config.max_tokens
                }
            })
        
        max_retries = 3
        retry_delay = 10
        
        for retry_count in range(max_retries):
            try:
                client = AsyncInferenceClient()
                batch_results = asyncio.run(client.send_batch(tasks))
                
                for result in batch_results:
                    if "id" in result and ("result" in result or "answer" in result):
                        task_idx = int(result["id"])
                        original_idx = to_process_indices[task_idx]
                        generated_text = result.get("result", result.get("answer", ""))
                        
                        results[original_idx] = generated_text
                        
                        if self.use_cache:
                            self.cache.set(to_process[task_idx], generated_text)
                
                break
                
            except Exception as e:
                error_msg = f"Batch processing failed (Attempt {retry_count + 1}/{max_retries}): {str(e)}"
                print(error_msg)
                
                if retry_count < max_retries - 1:
                    print(f"Waiting {retry_delay} seconds for retry...")
                    time.sleep(retry_delay)
                else:
                    print("All batch retries failed.")
                    for i, res in enumerate(results):
                        if res is None:
                            results[i] = ""
        
        for i, res in enumerate(results):
            if res is None:
                results[i] = ""
                
        self.save_cost()
        return results

    def _update_cost(self, input_tokens, output_tokens):
        """Update cumulative token count and cost"""
        self.total_input_tokens += input_tokens
        self.total_output_tokens += output_tokens

        in_rate = self.INPUT_COST_PER_1000_TOKENS.get(self.model_name)
        out_rate = self.OUTPUT_COST_PER_1000_TOKENS.get(self.model_name)

        if in_rate is None or out_rate is None:
            for key in self.INPUT_COST_PER_1000_TOKENS.keys():
                if key in str(self.model_name):
                    in_rate = self.INPUT_COST_PER_1000_TOKENS.get(key, in_rate)
                    break
            for key in self.OUTPUT_COST_PER_1000_TOKENS.keys():
                if key in str(self.model_name):
                    out_rate = self.OUTPUT_COST_PER_1000_TOKENS.get(key, out_rate)
                    break

        if in_rate is None or out_rate is None:
            mn = str(self.model_name)
            if mn not in self._warned_missing_cost:
                print(f"Warning: Missing pricing for model '{mn}'. Token cost calculated as 0.")
                self._warned_missing_cost.add(mn)
            in_rate = in_rate or 0.0
            out_rate = out_rate or 0.0

        cost = (input_tokens / 1000.0) * in_rate + (output_tokens / 1000.0) * out_rate
        self.total_cost += cost


    def save_cost(self):
        """Save cumulative cost information to cost.jsonl and reset counters"""
        current_model = str(self.model_name)
        add_input = int(self.total_input_tokens)
        add_output = int(self.total_output_tokens)
        add_cost = float(self.total_cost)

        cost_file = os.path.join(os.path.expanduser("~"), "cost.jsonl")
        
        agg: dict[str, dict] = {}
        try:
            if os.path.exists(cost_file):
                with open(cost_file, "r") as f:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            rec = json.loads(line)
                        except Exception:
                            continue
                        model_key = str(rec.get("model", "unknown"))
                        tin = int(rec.get("total_input_tokens", 0) or 0)
                        tout = int(rec.get("total_output_tokens", 0) or 0)
                        tcost = float(rec.get("total_cost", 0.0) or 0.0)
                        if model_key not in agg:
                            agg[model_key] = {
                                "model": model_key,
                                "total_input_tokens": 0,
                                "total_output_tokens": 0,
                                "total_cost": 0.0,
                            }
                        agg[model_key]["total_input_tokens"] += tin
                        agg[model_key]["total_output_tokens"] += tout
                        agg[model_key]["total_cost"] += tcost
        except Exception as e:
            print(f"Warning: Failed to load existing cost.jsonl: {e}")

        if current_model not in agg:
            agg[current_model] = {
                "model": current_model,
                "total_input_tokens": 0,
                "total_output_tokens": 0,
                "total_cost": 0.0,
            }
        agg[current_model]["total_input_tokens"] += add_input
        agg[current_model]["total_output_tokens"] += add_output
        agg[current_model]["total_cost"] += add_cost

        try:
            with open(cost_file, "w") as f:
                for _, rec in agg.items():
                    json.dump(rec, f)
                    f.write("\n")
        except Exception as e:
            print(f"Warning: Failed to write aggregated cost.jsonl: {e}")

        saved = agg[current_model]
        print(f"Saved cost: {saved}")
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_cost = 0
        return saved