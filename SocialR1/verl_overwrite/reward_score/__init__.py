import os
import logging
from typing import Dict, Any, List, Tuple, Optional, Union
from .utils_metric import DATASOURCE_METRICS
from . import qa_em_and_format
from collections import defaultdict
import re
import math

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("reward_score")

def _get_datasource_config(data_source): 
    ds_name = data_source[0] if isinstance(data_source, (list, tuple)) else data_source
    if ds_name == "socialR0":
        return {"metrics": ["em", "format"]}
    
    if data_source in DATASOURCE_METRICS:
        return DATASOURCE_METRICS[data_source]
    for key, config in DATASOURCE_METRICS.items():
        if key in data_source:
            return config
    logger.warning(f"Unknown data source: {data_source} ")
    return DATASOURCE_METRICS['mss']

def _extract_answer(solution_str, data_source):
    if solution_str is None: return ""
    try:
        from . import llm_evaluate
        return llm_evaluate.get_answer(solution_str)
    except Exception as e:
        logger.error(f"Answer extraction failed: {e}")
        return ""

def _compute_format_score(solution_str, data_source):
    if solution_str is None: return 0.0
    try:
        from . import llm_evaluate
        return llm_evaluate.compute_score_format(solution_str, data_source)
    except Exception as e:
        logger.error(f"Format score computation failed: {e}")
        return 0.0

def get_repetition_penalty(text, n=16):
    if not text or len(text) < n: return 1.0, 0.0
    grams = [text[i:i+n] for i in range(len(text)-n+1)]
    repeat_ratio = (len(grams) - len(set(grams))) / len(grams)
    penalty = 1.0 if repeat_ratio <= 0.1 else math.exp(-8.0 * (repeat_ratio - 0.1))
    return penalty, repeat_ratio

def get_window_length_penalty(content_length, l_min=400, l_max=2500):
    steepness = 50 
    low_gate = 1.0 / (1.0 + math.exp(-(content_length - l_min) / steepness))
    high_gate = 1.0 / (1.0 + math.exp((content_length - l_max) / steepness))
    return low_gate * high_gate

def get_annealed_weight(step, T=200.0, start_val=2.0, end_val=1.0):
    progress = min(1.0, step / T)
    return start_val + (end_val - start_val) * progress

def compute_score(data_source, solution_str, ground_truth, extra_info=None):
    is_batch = isinstance(solution_str, (list, tuple))
    if not is_batch:
        solution_str, ground_truth, data_source = [solution_str], [ground_truth], [data_source]
        extra_info = [extra_info if extra_info is not None else {}]
    
    num_items = len(solution_str)
    if not isinstance(ground_truth, (list, tuple)): ground_truth = [ground_truth] * num_items
    if extra_info is None: extra_info = [{}] * num_items
    elif not isinstance(extra_info, (list, tuple)): extra_info = [extra_info] * num_items
    if not isinstance(data_source, (list, tuple)): data_source = [data_source] * num_items

    all_items_data = []
    llm_groups = {} 

    for i in range(num_items):
        config = _get_datasource_config(data_source[i])
        item_data = {
            "original_index": i,
            "config": config,
            "solution_str": solution_str[i],
            "ground_truth": ground_truth[i],
            "extra_info": extra_info[i],
            "metrics": {},
            "data_source": data_source[i]
        }
        all_items_data.append(item_data)
        
        if 'llm' in config.get('metrics', []):
            mode = config.get('llm_mode', 'social_reasoning')
            if mode not in llm_groups: llm_groups[mode] = []
            llm_groups[mode].append(item_data)
 
    for mode, group_items in llm_groups.items():
        batch_questions = [item["extra_info"].get("question", "") for item in group_items]
        batch_answers = [_extract_answer(item["solution_str"], item["data_source"]) for item in group_items]
        batch_ground_truth = [item["ground_truth"] for item in group_items]
        batch_extra_info = [item["extra_info"] for item in group_items]
        
        try:
            from . import llm_evaluate
            batch_results = llm_evaluate.evaluate_model_answer(
                question=batch_questions, answer=batch_answers,
                ground_truth=batch_ground_truth, modes=[mode] * len(group_items),
                extra_info=batch_extra_info
            )
            for i, item in enumerate(group_items):
                res = batch_results[i]
                if isinstance(res, (list, tuple)) and len(res) == 4:
                    s_rm, s_gpt, r_rm, r_gpt = res
                    item["metrics"]["llm_rm_raw"] = float(s_rm)
                    item["metrics"]["llm_gpt_raw"] = float(s_gpt)
                elif isinstance(res, (list, tuple)) and len(res) == 2:
                    score, reason = res
                    if mode in ["socialR3", "social_r3"]:
                        item["metrics"]["llm_rm_raw"] = float(score)
                        item["metrics"]["llm_gpt_raw"] = 0.0
                    else:
                        item["metrics"]["llm_gpt_raw"] = float(score)
                        item["metrics"]["llm_rm_raw"] = 0.0
                item["metrics"]["llm"] = item["metrics"].get("llm_rm_raw", item["metrics"].get("llm_gpt_raw", 0.0))
        except Exception as e:
            logger.error(f"Batch LLM evaluation failed mode='{mode}': {e}")
            for item in group_items:
                item["metrics"]["llm_rm_raw"] = 0.0
                item["metrics"]["llm_gpt_raw"] = 0.0

    processed_results_data = []

    for i in range(num_items):
        item_data = all_items_data[i]
        current_metrics = item_data["metrics"].copy()
        ds = item_data["data_source"]
        config = item_data["config"]
        metrics_list = config.get('metrics', [])
        
        raw_answer = _extract_answer(item_data["solution_str"], ds)
        answer = raw_answer
        
        if ds in ["socialR0","socialR1", "socialR2", "socialR3", "socialR4", "socialR5", "ToM-RL"]:
            match = re.search(r"<Answer>\s*([A-Z])[\s\S]*?</Answer>", raw_answer)
            answer = match.group(1).strip() if match else ""
        elif ds in ["socsci", "item_selection", "socialr1"]:
            match = re.search(r'^<think>(.*?)</think>(.*?)$', raw_answer, re.DOTALL)
            answer = match.group(2).strip() if match else ""

        current_metrics["format"] = _compute_format_score(item_data["solution_str"], ds)
        if 'em' in metrics_list:
            current_metrics["em"] = qa_em_and_format.em_check(answer, item_data["ground_truth"], ds)
        
        solution_str = item_data.get("solution_str", "")
        think_match = re.search(r'<think>(.*?)</think>', solution_str, re.DOTALL)
        thought_content = think_match.group(1).strip() if think_match else ""
        effective_think_len = len(thought_content)

        rp_factor, repeat_ratio = get_repetition_penalty(thought_content)
        lp_factor = get_window_length_penalty(effective_think_len, l_min=400, l_max=3000)
        
        global_step = float(item_data["extra_info"].get("global_steps", 0))
        em_score = float(current_metrics.get("em", 0.0))
        format_score = float(current_metrics.get("format", 0.0))
        structure_score = float(current_metrics.get('llm_gpt_raw', 0.0))
        content_score = float(current_metrics.get('llm_rm_raw', 0.0))
        
        # Curriculum Learning Weights
        w_struct = get_annealed_weight(global_step, T=200, start_val=2.0, end_val=1.0)
        w_content = get_annealed_weight(global_step, T=200, start_val=1.0, end_val=3.0)
         reasoning_part = tau * (
                 w_struct * structure_score + 
                 w_content * adj_content
            )
        tau = 1.0 if em_score > 0.5 else 0.2
     combined_score = r_fmt * (em_score + reasoning_part)

        r_fmt = math.pow(format_score, 3)
        r_len = lp_factor * rp_factor
        adj_content = math.pow(max(0.0, content_score + 2), 1.2)

        if ds == "socialR0":
            combined_score = em_score + format_score
        elif ds in ["socialR1", "socialR2", "socialR3", "socialR4"]:
            use_struct = 1.0 if ds in ["socialR1", "socialR2", "socialR4"] else 0.0
            use_content = 1.0 if ds in ["socialR1", "socialR3", "socialR4"] else 0.0
            
            reasoning_part = tau * (
                use_struct * w_struct * structure_score + 
                use_content * w_content * adj_content
            )
            
            combined_score = r_fmt * (em_score + reasoning_part)
            
            if ds != "socialR4":
                combined_score *= r_len
                
            combined_score = 0.0 if format_score < 0.1 else max(0.01, combined_score)
        else:
            combined_score = em_score * 0.5 + format_score * 0.5
 
        result_dict = {
            "score": combined_score,
            "em": em_score,
            "llm_content": content_score,
            "llm_struct": structure_score,
            "format": format_score,
            "lp_factor": lp_factor,
            "rp_factor": rp_factor,
            "think_len": float(effective_think_len),
        }
        current_metrics.update(result_dict)
        processed_results_data.append(current_metrics)

    all_keys = set().union(*(d.keys() for d in processed_results_data))
    final_results = [{k: d.get(k, 0.0) for k in all_keys} for d in processed_results_data]
    return final_results if is_batch else final_results[0]

def default_compute_score(data_source, solution_str, ground_truth, extra_info=None, **kwargs):
    return compute_score(data_source, solution_str, ground_truth, extra_info)

__all__ = ["default_compute_score"]