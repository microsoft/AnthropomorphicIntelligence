# Copyright 2024 Bytedance Ltd. and/or its affiliates
# Copyright 2026 Social-R1 Contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re
import string
import json
import os
from typing import Dict, Any
try:
    from .templates import PromptTemplateManager
except ImportError:
    from templates import PromptTemplateManager
default_prompt_manager = PromptTemplateManager.get_instance()
RLMODEL = os.getenv("RLMODEL", "qwen25")
def normalize_answer(s):
    # def remove_articles(text):
    #     return re.sub(r"\b(a|an|the)\b", " ", text)

    def white_space_fix(text):
        return " ".join(text.split())

    def remove_punc(text):
        exclude = set(string.punctuation)
        return "".join(ch for ch in text if ch not in exclude)

    def lower(text):
        return text.lower()

    return white_space_fix(remove_punc(lower(s))).strip()


def em_check(prediction, golden_answers, data_source=None):
    if isinstance(golden_answers, str):
        golden_answers = [golden_answers]
    normalized_prediction = normalize_answer(prediction)
    score = 0.0
    for golden_answer in golden_answers:
        golden_answer = normalize_answer(golden_answer)
        if golden_answer == normalized_prediction:
            score = 1.0
            break
        if data_source == 'ToM-RL':
            ans_pattern = r".*?" + re.escape(golden_answer) + r"\s*\b$"
            if re.match(ans_pattern, normalized_prediction):
                score = 1.0
                break
    return score


def subem_check(prediction, golden_answers):
    if isinstance(golden_answers, str):
        golden_answers = [golden_answers]
    normalized_prediction = normalize_answer(prediction)
    score = 0.0
    for golden_answer in golden_answers:
        golden_answer = normalize_answer(golden_answer)
        if golden_answer in normalized_prediction:
            score = 1.0
            break
    return score


def extract_solution(solution_str):
    """Extract the answer from the solution string."""
    answer_pattern = r'<answer>(.*?)</answer>'
    match = re.search(answer_pattern, solution_str, re.DOTALL)
    
    if match:
        return match.group(1).strip()
    return ""

def compute_score_format(solution_str):
    """The scoring function for format reward.

    Args:
        solution_str: the solution text
    
    """
    if solution_str is None:
        return 0.0
    
    # If NO_THINK environment variable is set to true, return 1.0 score directly
    if os.getenv("NO_THINK", "false").lower() == "true":
        return 1.0
    
    try:
        # Perfect format match for the new structure
        # First <|im_start|>assistant should have <think> and possibly <tool_call>
        # Then <|im_start|>tool with <tool_response> (can repeat with assistant/tool pairs)
        # Final <|im_start|>assistant with the answer and <|im_end|>
        
        # Check for basic structure with <|im_start|>assistant and <|im_end|> tags
        assistant_blocks = default_prompt_manager.templates.get(RLMODEL).extract_role_blocks(solution_str, "assistant")

        format_reward = 0.0
        
        # If no blocks found, return 0
        if not assistant_blocks or len(assistant_blocks) == 0:
            return 0.0
        # Perfect format requires at least one assistant block and matching tool blocks if tool calls exist
        # Check first assistant block contains <think> tags
        for i, assistant_block in enumerate(assistant_blocks[:-1]):
            if assistant_block.count('<think>') == 1 and assistant_block.count('</think>') == 1 and assistant_block.count('<tool_call>') == 1 and assistant_block.count('</tool_call>') == 1:
                think_match = re.search(r'^<think>(.*?)</think>(\s*)<tool_call>(.*?)</tool_call>$', assistant_block, re.DOTALL)
                # soft_think_match = re.search(r'<think>(.*?)</think>(.*?)<tool_call>(.*?)</tool_call>', assistant_block, re.DOTALL)
                if think_match:
                    format_reward += 0.5 / (len(assistant_blocks) - 1)
                    # format_reward += 0.5

        # Check the last assistant block contains <answer> tags
        last_assistant_block = assistant_blocks[-1]
        think_answer_match = re.search(r'^<think>(.*?)</think>(.*?)<answer>(.*?)</answer>$', last_assistant_block, re.DOTALL)
        if think_answer_match:
            format_reward += 0.5
    except Exception as e:
        print(f"[DEBUG] Error in compute_score_format: {e}")
        return 0.0
    
    return format_reward

def compute_score_em(solution_str, ground_truth):
    """The scoring function for exact match (EM).

    Args:
        solution_str: the solution text
        ground_truth: the ground truth
    
    """
    if solution_str is None or ground_truth is None:
        return 0.0
    
    try:
        assistant_blocks = default_prompt_manager.templates.get(RLMODEL).extract_role_blocks(solution_str, "assistant")
        if not assistant_blocks or len(assistant_blocks) == 0:
            return 0.0
        solution_str = assistant_blocks[-1]
        answer = extract_solution(solution_str)
        if answer is None:
            return 0.0
        return float(subem_check(answer, ground_truth))
    except Exception as e:
        print(f"[DEBUG] Error in compute_score_em: {e}")
        return 0.0

def get_answer(solution_str):
    if solution_str is None:
        return ""
    try:
        assistant_blocks = default_prompt_manager.templates.get(RLMODEL).extract_role_blocks(solution_str, "assistant")
        if not assistant_blocks or len(assistant_blocks) == 0:
            return ""
        solution_str = assistant_blocks[-1]
        answer = extract_solution(solution_str)
        return answer if answer is not None else ""
    except Exception as e:
        print(f"[DEBUG] Error in get_answer: {e}")
        return ""