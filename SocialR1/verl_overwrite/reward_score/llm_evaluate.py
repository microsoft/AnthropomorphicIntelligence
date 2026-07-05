import re
import time
import os
import logging
from typing import Dict, Any, List, Union, Tuple, Optional
from concurrent.futures import ThreadPoolExecutor

from . import templates
default_prompt_manager = templates.PromptTemplateManager.get_instance()
RLMODEL = os.getenv("RLMODEL", "qwen25")

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("ModelEvaluator")

from . import llm_eval_prompt
get_prompt_by_mode = llm_eval_prompt.get_prompt_by_mode
prompt_map = llm_eval_prompt.prompt_map

class ModelEvaluator:
    # Hardcoded RM Prompt template (for port 8133)
    RM_PROMPT_TEMPLATE = """Evaluate whether the [Reasoning], given the [Story] and [Question], is human-like, uses social cues, logically consistent, and concise.\n{question}[Reasoning] {reasoning}"""

    def __init__(self, 
                 port_rm=int(os.getenv("LLM_SERVER_PORT_RM", 8133)), 
                 port_gpt=int(os.getenv("LLM_SERVER_PORT_GPT", 8134))):
        
        self.client_rm = None
        self.client_gpt = None
        self.executor = ThreadPoolExecutor(max_workers=2)

        try:
            import importlib.util
            # Assume correct path
            sync_client_path = os.path.join(os.path.dirname(__file__), 'AsyncInference', 'sync_client.py')
            spec = importlib.util.spec_from_file_location("sync_client", sync_client_path)
            sync_client = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(sync_client)
            
            # Initialize two clients
            self.client_rm = sync_client.SyncInferenceClient(port=port_rm)
            self.client_gpt = sync_client.SyncInferenceClient(port=port_gpt)
            logger.info(f"Successfully started Dual Judge Evaluator: RM({port_rm}) & GPT({port_gpt})")
        except Exception as e:
            logger.error(f"Failed to initialize SyncInferenceClient: {str(e)}")
            raise e
        
        self.supported_modes = prompt_map.keys()

    def _create_rm_prompt_internal(self, question: str, prediction: str) -> str:
        """Construct Prompt for port 8133 RM"""
        if hasattr(question, 'item') and callable(getattr(question, 'item', None)):
            question = question.item()
        question = str(question)

        # Extract <think> content
        answer_pattern = r'<think>(.*?)</think>'
        match = re.search(answer_pattern, prediction, re.DOTALL)
        reasoning = match.group(1).strip() if match else prediction
        return self.RM_PROMPT_TEMPLATE.format(question=question, reasoning=reasoning)

    def _parse_individual_result(self, result: str, mode: str) -> Tuple[float, str]:
        """Unified parsing logic"""
        try:
            # Note consistency of casing or underscores in mode mapping
            m = mode.lower()
            if m in ["social_r3", "socialr3"]:
                score = float(result)
                reason = ""
            elif m in ["social_r1", "social_r2", "social_r4", "social_r5", "socialr1", "socialr2", "socialr4", "socialr5"]:
                score = float(result.split("<Score>")[-1].split("</Score>")[0].strip()) if "<Score>" in result else float(result)
                reason = ""
            elif m in ["conversation", "writing", "social_qa", "persona", "socsci", "item_selection", "social_rm1"]:
                score = float(result.split("<score>")[-1].split("</score>")[0].strip())
                reason = ""
            elif m != "semantic_similarity":
                score = float(result.split("<score>")[-1].split("</score>")[0].strip()) / 5
                reason = result.split("<reason>")[-1].split("</reason>")[0].strip()
            else:
                score = float(result.split("<score>")[-1].split("</score>")[0].strip())
                reason = result.split("<reason>")[-1].split("</reason>")[0].strip()
            
            # Clamp range
            if m not in ["social_r1", "social_r3", "social_r4", "social_rm1", "socialr1", "socialr3", "socialr4"]:
                score = max(0.0, min(1.0, score))
            return score, reason
        except Exception as e:
            logger.warning(f"Parsing failed: {result}, Error: {e}")
            return 0.0, f"Error: {str(e)}"

    def batch_get_llm_judgment_scores_twollm(self, questions, predictions, golden_answers_list, modes=None, extra_info=None, metric='llm') -> List[Tuple[float, float, str, str]]:
        """
        Scheme A: Dual LLM Mode (targeting socialR1, socialR4)
        """
        if not isinstance(questions, (list, tuple)): questions = [questions]
        if not isinstance(predictions, (list, tuple)): predictions = [predictions]
        if not isinstance(golden_answers_list, (list, tuple)): golden_answers_list = [golden_answers_list]
        if modes is None: modes = ["socialR1"] * len(questions)
        if extra_info is None: extra_info = [None] * len(questions)

        prompts_rm = []
        prompts_gpt = []

        for i in range(len(questions)):
            q, p, g, m = questions[i], predictions[i], golden_answers_list[i], modes[i]
            ex = extra_info[i] if i < len(extra_info) else None
            prompts_rm.append(self._create_rm_prompt_internal(q, p))
            prompts_gpt.append(self._create_single_prompt(q, p, g, m, ex, metric))

        # Parallel requests to 8133 and 8134
        future_rm = self.executor.submit(self.client_rm.batch_predict, prompts_rm)
        future_gpt = self.executor.submit(self.client_gpt.batch_predict, prompts_gpt)

        res_rm_raw = future_rm.result()
        res_gpt_raw = future_gpt.result()

        final_results = []
        for i in range(len(questions)):
            # Port 8133 parsing (fixed to social_r3 logic for score parsing)
            s_rm, r_rm = self._parse_individual_result(res_rm_raw[i], mode="social_r3")
            # Port 8134 parsing (using original mode)
            s_gpt, r_gpt = self._parse_individual_result(res_gpt_raw[i], modes[i])
            final_results.append((s_rm, s_gpt, r_rm, r_gpt))

        return final_results

    def batch_get_llm_judgment_scores(self, questions, predictions, golden_answers_list, modes=None, extra_info=None, metric='llm') -> List[Tuple[float, str]]:
        """
        Scheme B: Single LLM Mode
        - social_r3 -> Port 8133 (RM)
        - social_r2/others -> Port 8134 (GPT)
        """
        if not isinstance(questions, (list, tuple)): questions = [questions]
        if not isinstance(predictions, (list, tuple)): predictions = [predictions]
        if not isinstance(golden_answers_list, (list, tuple)): golden_answers_list = [golden_answers_list]
        if modes is None: modes = ["social_reasoning"] * len(questions)
        if extra_info is None: extra_info = [None] * len(questions)

        # Determine current batch mode
        current_mode = modes[0].lower() if modes else ""
        
        # --- Routing Logic ---
        # Route to 8133 (RM) if socialR3
        if current_mode in ["social_r3", "socialr3"]:
            client = self.client_rm
            target_port = "8133 (RM)"
            prompts = [self._create_rm_prompt_internal(questions[i], predictions[i]) for i in range(len(questions))]
        
        # Route to 8134 (GPT) if socialR2 or other
        else:
            client = self.client_gpt
            target_port = "8134 (GPT)"
            prompts = [self._create_single_prompt(questions[i], predictions[i], golden_answers_list[i], modes[i], extra_info[i], metric) for i in range(len(questions))]

        logger.info(f"Single LLM eval mode: {current_mode}, Port: {target_port}")
        
        # Execute request
        batch_results = client.batch_predict(prompts)
        
        final_results = []
        for i in range(len(questions)):
            # Parsing logic still depends on specific modes
            res = self._parse_individual_result(batch_results[i], modes[i])
            final_results.append(res)
        return final_results

    def _create_single_prompt(self, question: str, prediction: str, golden_answers: Any, mode="social_reasoning", extra_info: Optional[Dict[str, Any]] = None, metric='llm') -> str:
        """Construct prompt logic (maintaining original behavior)"""
        if hasattr(question, 'item') and callable(getattr(question, 'item', None)):
            question = question.item()
        question = str(question)
        if not isinstance(prediction, str): prediction = str(prediction)

        # Handle golden_answers
        if isinstance(golden_answers, list):
            golden_answers = " or ".join([str(g) for g in golden_answers])
        
        try:
            # Map mode to prompt_map
            use_mode = mode
            if mode not in self.supported_modes:
                use_mode = "social_reasoning"
                
            prompt_template = get_prompt_by_mode(use_mode, metric)
            
            # Extract reasoning based on mode
            if mode.lower() in ['social_r0','social_r1','social_r2','social_r3','social_r4','social_r5', 'socialr0','socialr1', 'socialr2', 'socialr3', 'socialr4', 'socialr5']:
                answer_pattern = r'<think>(.*?)</think>'
                match = re.search(answer_pattern, prediction, re.DOTALL)
                reasoning = match.group(1).strip() if match else prediction
                format_dict = {"question": question, "reasoning": reasoning}
            elif mode.lower() == 'social_rm1':
                answer_pattern = r'<\|think_begin\|>(.*?)<\|think_end\|>'
                match = re.search(answer_pattern, prediction, re.DOTALL)
                reasoning = match.group(1).strip() if match else prediction
                format_dict = {"question": question, "reasoning": reasoning}
            else:
                answer_pattern = r'^<think>(.*?)</think>(.*?)$'
                match = re.search(answer_pattern, prediction, re.DOTALL)
                if match:
                    reasoning, answer = match.group(1).strip(), match.group(2).strip()
                else:
                    reasoning, answer = "No reasoning", "None"
                format_dict = {
                    "instruction": question,
                    "ground_truth": golden_answers,
                    "model_answer": answer if metric=="llm_outcome" else reasoning,
                }
            return prompt_template.format(**format_dict)
        except Exception as e:
            logger.error(f"Failed to create prompt: {e}")
            return f"Question: {question}\nAnswer: {prediction}" # Fallback

def evaluate_model_answer(question, answer, ground_truth, modes=None, extra_info=None, metric='llm'):
    """
    Entry point: Auto-select between Dual or Single LLM evaluation based on mode
    """
    evaluator = ModelEvaluator()
    
    # 1. Ensure list format
    is_batch = isinstance(question, (list, tuple))
    questions = question if is_batch else [question]
    answers = answer if is_batch else [answer]
    gts = ground_truth if is_batch else [ground_truth]
    
    # Process ground_truth format
    processed_gts = []
    for gt in gts:
        if isinstance(gt, dict):
            processed_gts.append(gt.get('target', []))
        else:
            processed_gts.append(gt)
            
    # 2. Determine Mode
    # Assumes mode is consistent within a single batch
    current_mode = modes[0] if isinstance(modes, (list, tuple)) else (modes if modes else "social_reasoning")

    # 3. Dispatch Logic
    # If mode is socialR1 or socialR4, use Dual LLM
    if current_mode in ["socialR1", "socialR4", "social_r1", "social_r4"]:
        results = evaluator.batch_get_llm_judgment_scores_twollm(
            questions, answers, processed_gts, modes, extra_info, metric
        )
   
    else:
        # Otherwise (including socialR2, socialR3), use Single LLM
        results = evaluator.batch_get_llm_judgment_scores(
            questions, answers, processed_gts, modes, extra_info, metric
        )
    
    return results if is_batch else results[0]



def compute_score_format(solution_str, data_source):
    """The scoring function for format reward.

    Args:
        solution_str: the solution text
    """
    if solution_str is None:
        return 0.0
    if os.getenv("NO_THINK", "false") == "true":
        return 1.0
    try:
        assistant_blocks = [solution_str]
        format_reward = 0.0
        
        # If no blocks found, return 0
        if not assistant_blocks or len(assistant_blocks) == 0:
            return 0.0
        last_assistant_block = assistant_blocks[-1]
        
        # Check the last assistant block contains <Answer> tags for specific sources
        if data_source in ["socialR0","socialR1", "socialR2", "socialR3", "socialR4", "socialR5", "socialRM1","ToM-RL"]:
            think_answer_match = re.search(r'^<think>(.*?)</think>(.*?)<Answer>(.*?)</Answer>$', last_assistant_block, re.DOTALL)
        else:
            think_answer_match = re.search(r'^<think>(.*?)</think>(.*?)$', last_assistant_block, re.DOTALL)
            
        if think_answer_match:
            format_reward = 1.0
    except Exception as e:
        print(f"[DEBUG] Error in compute_score_format: {e}")
        return 0.0
    
    return format_reward

def extract_solution(solution_str):
    """Extract the answer from the solution string."""
    if os.getenv("NO_THINK", "false").lower() == "true":
        return solution_str

    answer_pattern = r'<answer>(.*?)</answer>'
    match = re.search(answer_pattern, solution_str, re.DOTALL)
    
    if match:
        return match.group(1).strip()
    return ""


def get_answer(solution_str):
    # verl automatically extracts answers now
    return solution_str