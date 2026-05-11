# -*- coding: utf-8 -*-
"""
Various prompt templates for evaluating model outputs
"""

# Social reasoning evaluation template
SOCIAL_REASONING_PROMPT = """You are given a question, a **reference answer** (which is a very high-quality response to the question), and a **model's response**. Your task is to assess the quality of the model's response to the question, using the reference answer as a benchmark. Please consider that the question may be open-ended, and there can be multiple high-quality responses—not only the reference answer.  
   
Please assign an integer score from 0 to 5 according to the following criteria:  
   
**0 (Totally Incorrect)**    
The response is completely incorrect. It is irrelevant, nonsensical, contains major logical errors, contradictions, or demonstrates a lack of understanding of the question.  
   
**1 (Poor)**    
The response shows partial relevance but contains significant errors, misunderstandings, or omissions. It does not adequately address the main points of the question.  
   
**2 (Fair)**    
The response is related to the question and contains some correct information, but has notable gaps, incomplete reasoning, or minor errors that detract from its overall quality.  
   
**3 (Good)**    
The response is mostly correct and relevant, satisfactorily addressing the question. However, it is not as thorough, clear, or accurate as the reference answer. Some minor aspects may be missing or less well-explained.  
   
**4 (Very Good / Comparable to Reference)**    
The response is of very high quality. It matches the reference answer in correctness, completeness, and clarity, though it may use different wording or approach. Any differences are small and do not detract from the overall quality.  
   
**5 (Excellent / Better than Reference)**    
The response is of exceptional quality, surpassing the reference answer by providing additional valuable insights, greater clarity, or a more comprehensive explanation.  
   
---  
   
**Instructions:**  
   
- Base your evaluation primarily on the model's response to the question, referencing the reference answer as a standard.  
- Give full credit (score of 4) for answers matching the reference answer in quality, even if phrased differently.  
- Assign a score of 5 only if the response is clearly better—more informative, accurate, nuanced, or insightful—than the reference answer.  
  
   
Output your answer in the XML format:  

<reason> [a very short explanation] </reason>
<score> [an integer from 0 to 5] </score>

Now the task begins. 
Below is the original question. 
------
{question}  
------
Below is the reference answer:
------
{golden_answers}
------
Below is the model's answer that needs evaluation:
------
{prediction}
------ 
Please only output the XML result."""

# Factual accuracy evaluation template
FACTUAL_ACCURACY_PROMPT = """You are an expert fact-checker. Your task is to evaluate the factual accuracy of a model's response to a question, comparing it to a reference answer that is known to be factually correct.

Please assign an integer score from 0 to 5 according to the following criteria:

**0 (Completely Inaccurate)**
The response contains critical factual errors or completely misrepresents the facts.

**1 (Mostly Inaccurate)**
The response contains multiple factual errors, though it may have some correct information.

**2 (Partially Accurate)**
The response has a mix of correct and incorrect factual information, with significant omissions or errors.

**3 (Mostly Accurate)**
The response is largely factually correct but has minor errors or omissions.

**4 (Highly Accurate)**
The response is factually accurate and matches the reference answer in all important aspects.

**5 (Perfectly Accurate)**
The response is completely factually accurate, possibly including additional correct facts beyond the reference answer.

---

**Instructions:**
- Focus exclusively on factual accuracy, not writing style or presentation.
- Compare specific facts, dates, numbers, names, and relationships mentioned in both answers.
- Do not penalize for additional correct information not in the reference answer.

Output your answer in the XML format:

<reason> [a brief explanation of your evaluation] </reason>
<score> [an integer from 0 to 5] </score>

Now the task begins.
Below is the original question:
------
{question}
------
Below is the reference answer (factually correct):
------
{golden_answers}
------
Below is the model's answer that needs evaluation:
------
{prediction}
------
Please only output the XML result."""

# Math problem evaluation template
MATH_PROBLEM_PROMPT = """You are a mathematics expert evaluating the correctness of a solution to a math problem. Your task is to assess whether the model's solution reaches the correct answer and follows a valid mathematical approach.

Please assign an integer score from 0 to 5 according to the following criteria:

**0 (Completely Incorrect)**
The solution uses an invalid approach and reaches an incorrect answer.

**1 (Incorrect Approach)**
The solution uses a fundamentally flawed approach with serious mathematical errors.

**2 (Partially Correct)**
The solution shows some understanding of the problem but contains significant errors in the approach or calculation.

**3 (Mostly Correct)**
The solution uses a valid approach with minor errors that affect the final answer.

**4 (Correct Answer)**
The solution reaches the correct answer using a valid mathematical approach.

**5 (Exemplary Solution)**
The solution is not only correct but demonstrates exceptional clarity, efficiency, or insight.

---

**Instructions:**
- Focus primarily on mathematical correctness and validity of the approach.
- Check for calculation errors, conceptual misunderstandings, and logical flaws.
- The final answer must match the reference solution to receive a score of 4 or higher.

Output your answer in the XML format:

<reason> [a brief explanation of your evaluation] </reason>
<score> [an integer from 0 to 5] </score>

Now the task begins.
Below is the original math problem:
------
{question}
------
Below is the reference solution (correct):
------
{golden_answers}
------
Below is the model's solution that needs evaluation:
------
{prediction}
------
Please only output the XML result."""

# Tool usage evaluation template
TOOL_USAGE_PROMPT = """You are evaluating how effectively a model uses tools to solve a problem. Your task is to assess whether the model correctly identifies when to use tools, uses them appropriately, and interprets their outputs correctly.

Please assign an integer score from 0 to 5 according to the following criteria:

**0 (No Tool Usage)**
The model fails to use tools when they are clearly needed, or uses completely irrelevant tools.

**1 (Poor Tool Usage)**
The model attempts to use tools but with major errors in tool selection, parameter specification, or output interpretation.

**2 (Basic Tool Usage)**
The model uses some appropriate tools but with notable inefficiencies, unnecessary calls, or misinterpretations of outputs.

**3 (Competent Tool Usage)**
The model uses appropriate tools with minor inefficiencies or occasional misinterpretations.

**4 (Skilled Tool Usage)**
The model uses tools effectively, with appropriate selection, parameters, and correct interpretation of outputs.

**5 (Expert Tool Usage)**
The model demonstrates exceptional tool usage, with optimal selection, parameters, and interpretation, possibly using creative combinations of tools.

---

**Instructions:**
- Focus on how effectively the model uses tools to solve the problem.
- Consider whether the model uses the right tools at the right time.
- Evaluate how well the model interprets and uses the information returned by tools.

Output your answer in the XML format:

<reason> [a brief explanation of your evaluation] </reason>
<score> [an integer from 0 to 5] </score>

Now the task begins.
Below is the original problem:
------
{question}
------
Below is the reference solution (with effective tool usage):
------
{golden_answers}
------
Below is the model's solution that needs evaluation:
------
{prediction}
------
Please only output the XML result."""

# Comprehensive evaluation template
COMPREHENSIVE_PROMPT = """You are evaluating the overall quality of a model's response to a question. Your task is to assess the response based on multiple dimensions: factual accuracy, relevance, completeness, and clarity.

Please assign an integer score from 0 to 5 according to the following criteria:

**0 (Unacceptable)**
The response is completely off-topic, factually incorrect, or incomprehensible.

**1 (Poor)**
The response has major deficiencies in multiple dimensions (accuracy, relevance, completeness, clarity).

**2 (Fair)**
The response addresses the question but has significant gaps or errors.

**3 (Good)**
The response is mostly accurate, relevant, and clear, with minor shortcomings.

**4 (Very Good)**
The response is accurate, relevant, complete, and clear, comparable to the reference answer.

**5 (Excellent)**
The response exceeds expectations in all dimensions, possibly surpassing the reference answer.

---

**Instructions:**
- Consider all aspects of the response: factual accuracy, relevance to the question, completeness, and clarity.
- Compare with the reference answer as a benchmark for quality.
- Evaluate based on the response's effectiveness in addressing the question.

Output your answer in the XML format:

<reason> [a brief explanation of your evaluation] </reason>
<score> [an integer from 0 to 5] </score>

Now the task begins.
Below is the original question:
------
{question}
------
Below is the reference answer:
------
{golden_answers}
------
Below is the model's answer that needs evaluation:
------
{prediction}
------
Please only output the XML result."""

# Roleplay evaluation template
ROLEPLAY_PROMPT = """You are a professional and strict dialogue critic in role-playing games. Your task is to evaluate a model-generated NPC response given a role-playing instruction and context. 
You must assess the response based on the following four dimensions:

---

### 1. Scenario Adherence & Quest Progression
- Does the NPC respond appropriately to the situation and task at hand?
- Does it help move the current quest, story, or dialogue forward?

**Common Flaws:**
- ❌ *Off-topic*: Irrelevant to quest or context.
- ❌ *Contradiction*: Conflicts with known facts, lore, or current state.
- ❌ *Stalling*: Provides no progression or new info.
- ❌ *Misunderstanding*: Misinterprets player intent or scenario goals.

---

### 2. NPC Believability & Engagement
- Does the response feel natural, immersive, and emotionally appropriate?
- Is the response engaging and does it maintain conversational flow?

**Common Flaws:**
- ❌ *Unnatural phrasing*: Robotic, overly formal/informal, generic AI tone.
- ❌ *Flat or emotionless*: No personality or mood.
- ❌ *Passive*: NPC only reacts, without showing curiosity or initiative.
- ❌ *Blandness*: Lacks charm or fails to make the scene interesting.

---

### 3. Persona Consistency (NPC Only)
- Is the NPC’s behavior, knowledge, and style consistent with their defined background and personality?
- Are they saying things that fit their role, identity, and motivations?

**Common Flaws:**
- ❌ *Out-of-character speech*: Unexpected tone, values, or actions.
- ❌ *Knowledge errors*: Knowing things they shouldn’t or forgetting key facts.
- ❌ *Role mismatch*: Behaving in a way their job/class/background would not support.
- ❌ *Motivational inconsistency*: Conflicting goals or emotional reactions.

---

### 4. Dialogue Flow & Coherence
- Is the response well-structured, logically coherent, and contextually relevant?

**Common Flaws:**
- ❌ *Non-sequitur*: Abrupt topic change or irrelevant reply.
- ❌ *Redundancy*: Repeats previous info without purpose.
- ❌ *Contradiction*: Breaks continuity within the turn or dialogue history.
- ❌ *Under- or over-explaining*: Too brief for context or overly verbose.

---

### Scoring Criteria (0-5):
| Score | Description |
|-------|-------------|
| **0** | Completely fails across all dimensions; irrelevant, incoherent, and unfit for the scenario. |
| **1** | Very weak response with multiple serious issues; major breaks in persona or flow. |
| **2** | Partial attempt; may fit scenario but have notable flaws in tone, style, or engagement. |
| **3** | Reasonably coherent and consistent, but lacks depth, creativity, or has minor lapses. |
| **4** | Strong response with only minor issues; consistent, engaging, and well-fitted to role. |
| **5** | Excellent across all aspects; immersive, emotionally rich, and convincingly in character. |

---

## Evaluation Instructions:
Please carefully evaluate the NPC response using the above dimensions and common flaw types.

Keep in mind that this is a **conversational scenario in a video game**, where players expect the NPC to be:

- **Concise and efficient**: NPC responses should be short and to the point. Lengthy or verbose responses may reduce engagement and harm the gameplay experience.
- **Verbal only**: The NPC’s output should include only spoken dialogue. Avoid any narrative descriptions or non-verbal commentary (e.g., "*He looks at you thoughtfully.*").

The answer should aim to reflect characteristics commonly found in high-quality roleplay outputs:

✅ **Positive Traits of High-Quality Roleplay Responses**:

1. **High Interactivity**  
   - ~24% of good responses end with a question, showing initiative and player engagement.  
   - Common prompt: *“Would you like to try…?”*

2. **Appropriate Emotional Expression**  
   - Use of emotional words (6%), exclamations (1.5%), and acknowledgment phrases (5.6%).  
   - Reflects a warm but professional tone, suitable for long-term NPC interactions.

3. **Semantic Relevance to RPG Setting**  
   - Frequent mentions of in-world concepts like weapons, quest items, and mechanics (e.g., *“short sword”*, *“attack level”*).  
   - Reinforces immersion and narrative consistency.

4. **Clear Structure and Template Consistency**  
   - Frequent use of structured phrases like *“Would you like to…”* enhances readability and coherence.  
   - Helps maintain tone consistency and minimizes errors.

5. **Concise but Informative**  
   - Average length ~31 tokens (range: 7–66), providing sufficient content without over-explaining.  
   - Balances brevity with clarity.

### Now the evaluation task begins.
Below is the original instruction and conversation history for the role-play:
------
{question}
------
Below is the reference normal response about score 3:
------
{golden_answers}
------
Below is the model's response that needs evaluation:
------
{prediction}
------
Please only output the XML result:
<reason> [a brief justification based on the four dimensions above] </reason>  
<score> [an integer from 0 to 5] </score>
"""

# Creative writing evaluation template
CREATIVE_WRITING_PROMPT = """You are evaluating the creative quality of a model's response to a writing prompt. Your task is to assess the originality, engagement, and overall quality of the writing.

Please assign an integer score from 0 to 5 according to the following criteria:

**0 (Not Creative)**
The response shows no creativity, is generic, clichéd, or completely misses the prompt.

**1 (Minimally Creative)**
The response shows very little creativity, with heavy reliance on common tropes or predictable elements.

**2 (Somewhat Creative)**
The response shows some creativity but remains largely conventional or underdeveloped.

**3 (Moderately Creative)**
The response demonstrates creativity with some original elements and decent engagement.

**4 (Highly Creative)**
The response is original, engaging, and well-crafted, comparable to the reference example.

**5 (Exceptionally Creative)**
The response shows exceptional creativity, with outstanding originality, engagement, and craft.

---

**Instructions:**
- Focus on creative elements: originality, imagination, engagement, and craft.
- Consider how well the response fulfills the creative intent of the prompt.
- Compare with the reference example as a benchmark for creative quality.

Output your answer in the XML format:

<reason> [a brief explanation of your evaluation] </reason>
<score> [an integer from 0 to 5] </score>

Now the evaluation task begins.
Below is the original prompt:
------
{question}
------
Below is the reference creative example:
------
{golden_answers}
------
Below is the model's creative response that needs evaluation:
------
{prediction}
------
Please only output the XML result."""

SEMANTIC_SIMILARITY_PROMPT = """You are a strict semantic equivalence judge for question-answering tasks like HotpotQA. Your task is to determine if a model's answer is STRICTLY SEMANTICALLY EQUIVALENT to the reference answer.

STRICT SEMANTIC EQUIVALENCE means:
- The model's answer must contain ALL the factual information present in the reference answer
- It may include additional information ONLY IF:
  - It does not contradict any part of the reference answer
  - It does not change the focus or meaning of the answer
- Different wording or phrasing is acceptable ONLY if the meaning remains identical
- Missing any part of the information in the reference answer means the answers are NOT equivalent
- Contradictions, factual inconsistencies, or shifts in meaning result in a score of 0
- Names, dates, numbers, and specific facts must match exactly in meaning

You must output ONLY a binary score:
- Score 1: The answers are strictly semantically equivalent
- Score 0: The answers are not strictly semantically equivalent

---

Now evaluate the following:

Question:
{question}

Reference Answer:
{golden_answers}

Model's Answer:
{prediction}

Provide your evaluation in this format ONLY:
<reason>Brief explanation of why the answers are equivalent or not</reason>
<score>0 or 1</score>
"""

SEMANTIC_SIMILARITY_PROMPT_KEEP_THINK = """You are a strict semantic equivalence judge for question-answering tasks. Your task is to determine if a model's answer is STRICTLY SEMANTICALLY EQUIVALENT to the reference answer.

STRICT SEMANTIC EQUIVALENCE means:
- The model's answer must contain ALL the factual information present in the reference answer
- It may include additional information ONLY IF:
  - It does not contradict any part of the reference answer
  - It does not change the focus or meaning of the answer
- Different wording or phrasing is acceptable ONLY if the meaning remains identical
- Missing any part of the information in the reference answer means the answers are NOT equivalent
- Contradictions, factual inconsistencies, or shifts in meaning result in a score of 0
- Names, dates, numbers, and specific facts must match exactly in meaning

ADDITIONAL RULES FOR ANSWERS IN <think>...</think>answer FORMAT:
- The answer section must be strictly semantically equivalent to the reference answer according to the criteria above
- The <think> section must contain reasonable and logically sound justification or reasoning; vague, illogical, or incoherent thinking leads to a score of 0
- If the output has no <think> section and only answer, the answer alone will be evaluated
- Any hallucination, repetition, or irrelevant content (nonsense or garbage) in either section leads to a score of 0

You must output ONLY a score between 0 and 1 (in increments of 0.1), representing the degree of semantic equivalence:
- Score 1.0: Perfect semantic equivalence
- Score 0.7–0.9: Mostly equivalent, with minor missing or redundant info that doesn’t affect core meaning
- Score 0.4–0.6: Partial equivalence, some important content missing or ambiguous
- Score 0.1–0.3: Low equivalence, major content missing or altered meaning
- Score 0: No semantic equivalence (contradictions, hallucinations, or irrelevant content)


---

Now evaluate the following:

Question:
{question}

Reference Answer:
{golden_answers}

Model's Answer:
{prediction}

Provide your evaluation in this format ONLY:
<reason>Brief explanation of why the answers are equivalent or not</reason>
<score>0 or 1</score>
"""

SOCIAL_R1_PROMPT = """
You are a Social Reasoning Logic Auditor. Your task is to evaluate the logical integrity of a provided [Reasoning] trajectory based on a specific [Story] and [Question].\n
Core Objective:\n
Determine if the [Reasoning] genuinely analyzes the social context or simply matches patterns to guess the answer. Focus on the logic flow, not the answer correctness.\n
1. Mandatory SIP Reasoning Stages\n
A high-quality reasoning process must follow this sequence:
- Stage 1: Encoding Social Cues: Extract verbal, emotional, and factual cues from the [Story].
- Stage 2: Interpreting Social Cues: Use world knowledge to infer mental states using Theory of Mind.
- Stage 3: Clarifying Social Goals: Identify the protagonist's primary motivation or social goal in the context of the [Story] & [Question].
- Stage 4: Generating a Response: Formulate a conclusion derived strictly from the analytical steps above.
\n
2. Audit Penalties \n
Lower the score if the [Reasoning] exhibits any of the following:\n
- Option Parasitism: The reasoning mentions options (e.g., Option A, Choice B) before the inference phase.
- Backward Justification: The logic starts from an answer and works backward to justify it.\n
- SIP Sequence Violation: Failing to follow the logical progression or skipping any of the mandatory stages in the analytical sequence.\n
-  SIP Step Looping: Redundantly revisiting or repeating specific analytical steps (e.g., returning to Stage 1 after reaching Stage 2, or circular repetition of Stage 2 without advancing the logic or adding new insights.\n


3. Scoring Scale [0.0 - 1.0]\n
- 0.0 to 0.3: Failed logic. Direct answer selection or lack of SIP structure.\n
- 0.4 to 0.6: Weak logic. Skips stages or shows high dependency on the multiple-choice format.\n
- 0.7 to 0.8: Solid logic. Follows the stages but contains redundancy or SIP Looping.\n
- 0.9 to 1.0: 0.9 to 1.0: Perfect logic. Concise, follows all four stages in a clear forward-chaining sequence without circularity.\n

4. Output Format
You must output the final score exclusively between <Score> tags. Do not provide any explanation, preamble, or additional text.
Example: <Score>0.85</Score>

{question}
[Reasoning]{reasoning}

Please only output the XML result. 

"""

SOCIAL_R2_PROMPT = """
You are a Social Reasoning Logic Auditor. Your task is to evaluate the logical integrity of a provided [Reasoning] trajectory based on a specific [Story] and [Question].\n
Core Objective:\n
Determine if the [Reasoning] genuinely analyzes the social context or simply matches patterns to guess the answer. Focus on the logic flow, not the answer correctness.\n
1. Mandatory SIP Reasoning Stages\n
A high-quality reasoning process must follow this sequence:
- Stage 1: Encoding Social Cues: Extract verbal, emotional, and factual cues from the [Story].
- Stage 2: Interpreting Social Cues: Use world knowledge to infer mental states using Theory of Mind.
- Stage 3: Clarifying Social Goals: Identify the protagonist's primary motivation or social goal in the context of the [Story] & [Question].
- Stage 4: Generating a Response: Formulate a conclusion derived strictly from the analytical steps above.
\n
2. Audit Penalties \n
Lower the score if the [Reasoning] exhibits any of the following:\n
- Option Parasitism: The reasoning mentions options (e.g., Option A, Choice B) before the inference phase.
- Backward Justification: The logic starts from an answer and works backward to justify it.\n
- SIP Sequence Violation: Failing to follow the logical progression or skipping any of the mandatory stages in the analytical sequence.\n
-  SIP Step Looping: Redundantly revisiting or repeating specific analytical steps (e.g., returning to Stage 1 after reaching Stage 2, or circular repetition of Stage 2 without advancing the logic or adding new insights.\n


3. Scoring Scale [0.0 - 1.0]\n
- 0.0 to 0.3: Failed logic. Direct answer selection or length of SIP structure.\n
- 0.4 to 0.6: Weak logic. Skips stages or shows high dependency on the multiple-choice format.\n
- 0.7 to 0.8: Solid logic. Follows the stages but contains redundancy or SIP Looping.\n
- 0.9 to 1.0: 0.9 to 1.0: Perfect logic. Concise, follows all four stages in a clear forward-chaining sequence without circularity.\n

4. Output Format
You must output the final score exclusively between <Score> tags. Do not provide any explanation, preamble, or additional text.
Example: <Score>0.85</Score>

{question}
[Reasoning]{reasoning}

Please only output the XML result. 

"""

SOCIAL_R3_PROMPT = """Evaluate whether the [Reasoning], given the [Story] and [Question], is human-like, uses social cues, logically consistent, and concise.\n{question}[Reasoning] {reasoning}"""

SOCIAL_R4_PROMPT = """
You are a Social Reasoning Logic Auditor. Your task is to evaluate the logical integrity of a provided [Reasoning] trajectory based on a specific [Story] and [Question].\n
Core Objective:\n
Determine if the [Reasoning] genuinely analyzes the social context or simply matches patterns to guess the answer. Focus on the logic flow, not the answer correctness.\n
1. Mandatory SIP Reasoning Stages\n
A high-quality reasoning process must follow this sequence:
- Stage 1: Encoding Social Cues: Extract verbal, emotional, and factual cues from the [Story].
- Stage 2: Interpreting Social Cues: Use world knowledge to infer mental states using Theory of Mind.
- Stage 3: Clarifying Social Goals: Identify the protagonist's primary motivation or social goal in the context of the [Story] & [Question].
- Stage 4: Generating a Response: Formulate a conclusion derived strictly from the analytical steps above.
\n
2. Audit Penalties \n
Lower the score if the [Reasoning] exhibits any of the following:\n
- Option Parasitism: The reasoning mentions options (e.g., Option A, Choice B) before the inference phase.
- Backward Justification: The logic starts from an answer and works backward to justify it.\n
- SIP Sequence Violation: Failing to follow the logical progression or skipping any of the mandatory stages in the analytical sequence.\n
-  SIP Step Looping: Redundantly revisiting or repeating specific analytical steps (e.g., returning to Stage 1 after reaching Stage 2, or circular repetition of Stage 2 without advancing the logic or adding new insights.\n


3. Scoring Scale [0.0 - 1.0]\n
- 0.0 to 0.3: Failed logic. Direct answer selection or lack of SIP structure.\n
- 0.4 to 0.6: Weak logic. Skips stages or shows high dependency on the multiple-choice format.\n
- 0.7 to 0.8: Solid logic. Follows the stages but contains redundancy or SIP Looping.\n
- 0.9 to 1.0: 0.9 to 1.0: Perfect logic. Concise, follows all four stages in a clear forward-chaining sequence without circularity.\n

4. Output Format
You must output the final score exclusively between <Score> tags. Do not provide any explanation, preamble, or additional text.
Example: <Score>0.85</Score>

{question}
[Reasoning]{reasoning}

Please only output the XML result. 

"""


REASONING_REWARD_PROMPT = """You are an expert reasoning evaluator. You will be given an input consisting of:
'=== Instruction ===', '=== Ground Truth Answer ===', and '=== Candidate Reasoning Process ==='.
Your task is to evaluate the Candidate Reasoning Process, focusing solely on the quality of reasoning —not the correctness of the final answer itself.

Evaluation Criteria:

1. Directional Alignment and Instruction Grounding – Does the reasoning move toward the Ground Truth Answer, and does it properly make use of the meaningful information in the Instruction?
   - Does the reasoning extract and use relevant cues from the Instruction (e.g., persona details, scenario information, constraints, or contextual signals)?
   - Is the thought process based on appropriate and informative parts of the Instruction rather than irrelevant or misinterpreted details?
   - Does the reasoning progress in a direction conceptually consistent with the Ground Truth Answer?

2. Logical Soundness – Is the reasoning coherent, internally consistent, and free of contradictions?
   - Are steps logically connected and meaningful?
   - Is the reasoning structured in a way that reflects deliberate, step-by-step thinking?

3. Conciseness and Efficiency – Is the reasoning clear and succinct?
   - Does it avoid unnecessary repetition, circular thinking, filler text, or rambling?
   - Does it express ideas in a focused manner without over-elaboration?

4. Human-like Thought Quality – Does the reasoning resemble a natural, purposeful human thought process?
   - Does it demonstrate appropriate interpretation, problem understanding, and purposeful progression?

Scoring Rule:
Give a single score from the set:
[0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

- 0.0 → Fundamentally flawed reasoning (irrelevant, incoherent, or nonsensical).
- 1.0 → Excellent reasoning (well-grounded, coherent, directionally correct, and efficient).
- Intermediate scores → Reflect partial strengths and weaknesses:
  (e.g., 0.3 for major flaws, 0.7 for mostly good reasoning with some issues).

Be strict: reward high-quality reasoning and penalize poor reasoning.

Output Format:
<score>xx</score>   (Example: <score>0.5</score>)

Now evaluate the following:

=== Instruction ===
{instruction}

=== Ground Truth Answer ===
{ground_truth}

=== Candidate Reasoning Process ===
{model_answer}

Please output only the XML result in <score>xx</score> format.
"""

SOCIAL_QA_PROMPT = """You are an expert evaluator for personalized Social QA tasks.  
You will be given:  
'=== Instruction ===', '=== Ground Truth Answer ===', and a '=== Model Answer ==='.  
Your task is to evaluate how well the Model Answer matches the Ground Truth Answer in meaning, relevance, and contextual grounding.

Evaluation Criteria:

1. Semantic Alignment & Completeness  
   - Does the Model Answer convey the same essential meaning as the Ground Truth?  
   - Does it correctly capture the key idea or causal explanation the question asks for?  
   - Minor wording differences are acceptable; missing or incorrect core meaning should be penalized.

2. Faithfulness to Context (Persona + Scenario)  
   - Is the answer compatible with the persona and scenario described in the Instruction?  
   - Does it avoid adding unsupported assumptions or contradicting contextual information?

3. Clarity and Style Compliance  
   - Does the answer follow the required style in the Instruction (e.g., third person, approximate length)?  
   - Is the response coherent and free of irrelevant content?

Scoring Rule:  
Assign one score from:  
[0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

- 1.0 → Strong semantic match; correct key meaning; contextually faithful; stylistically correct.  
- 0.0 → Incorrect or unrelated meaning; fails to answer the question.  
- Intermediate scores reflect partial correctness.

Output Format:  
<score>xx</score>   (Example: <score>0.5</score>)

Now evaluate the following:

=== Instruction ===
{instruction}

=== Ground Truth Answer === 
{ground_truth}

=== Model Answer === 
{model_answer}

Please output only the XML result in <score>xx</score> format.
"""

CONVERSATION_PROMPT = """You are an expert evaluator for personalized conversational agents.  
You will be given:  
'=== Instruction ===', '=== Ground Truth Response ===', and a '=== Model Response ==='.  
Your task is to evaluate how well the Model Response matches the target persona’s conversational style and behavioral tendencies, as described in the Instruction.

Evaluation Criteria:

1. Persona Consistency  
   - Does the response reflect the persona’s characteristic voice, tone, attitudes, and thinking style?  
   - Does it follow the same patterns shown in the prior turns (e.g., structure, enthusiasm level, humor style, typical references, depth of reasoning)?  
   - Does it sound like something this specific person would naturally say?

2. Conversational Appropriateness  
   - Is the response contextually relevant to the final user turn?  
   - Does it continue the conversation naturally and coherently?  
   - Avoids contradictions, non sequiturs, or ignoring key conversational cues.

3. Alignment With Instructional Constraints  
   - Does the response follow formatting, perspective, and any task-specific rules from the Instruction (e.g., produce the character's next utterance only)?  
   - Is the style appropriate (dialogue, not explanation)?

Scoring Rule:  
Assign one score from the set:  
[0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

- 1.0 → Strong persona match; natural continuation; highly faithful to style and tone.  
- 0.0 → Not in character; irrelevant; breaks persona or conversation.  
- Intermediate scores reflect partial alignment.

Important:  
Do NOT evaluate the response based on whether its content matches the Ground Truth.  
The Ground Truth only serves as an example of the persona’s style.  
Your evaluation should focus solely on how well the Model Response aligns with the persona’s voice, tone, and behavioral tendencies, and whether it naturally fits the conversational context.


Output Format:  
<score>xx</score>   (Example: <score>0.5</score>)

Now evaluate the following:

=== Instruction === 
{instruction}

=== Ground Truth Response ===
{ground_truth}

=== Model Response ===
{model_answer}

Please output only the XML result in <score>xx</score> format.
"""

PERSONALIZED_WRITING_PROMPT = """You are an expert evaluator for personalized writing.
You will be given:  
'=== Instruction ===', '=== Ground Truth Writing ===', and '=== Model Writing ==='.  
All information about the user’s writing style—whether in the form of past writings or an explicit style description—is contained inside the Instruction.  
Your job is to evaluate how well the Model Writing reflects the user’s unique writing voice and follows the task.

Evaluation Criteria:

1. Style & Voice Alignment  
   - Does the Model Writing faithfully imitate the writing style implied by the Instruction  
     (which may include past writings or a summarized writing-style description)?  
   - Consider tone, pacing, emotional depth, level of reflection, narrative structure, typical themes, and word choice.  
   - Does it “sound” like the same person who wrote or is described in the Instruction?

2. Topic Fulfillment & Content Relevance  
   - Does the Model Writing directly address the topic given in the Instruction?  
   - Is the content coherent, contextually appropriate, and aligned with what the task requires?  
   - Does it meaningfully develop and expand on the topic rather than drifting into unrelated themes?

3. Richness & Realistic Detail  
   - Does the Model Writing include vivid, believable, and natural-feeling details?  
   - The writing should demonstrate a depth and concreteness similar to what is shown or described in the Instruction.  
   - The details do NOT need to match the Ground Truth Writing, but should be comparable in texture and specificity.

4. Consistency With the User’s Persona / History  
   - The writing should not contradict information about the user that appears in the Instruction  
     (e.g., life context, beliefs, habits, relationships, emotional tendencies).  
   - It should feel like a natural continuation of how this user would normally write or express themselves.

Important Note:  
Do NOT evaluate based on similarity of content to the Ground Truth Writing.  
The Ground Truth serves only as an example of appropriate style richness and narrative depth.  
Your evaluation is based solely on:  
- persona-consistent style imitation,  
- topic relevance,  
- realistic detail quality,  
- and internal consistency with information in the Instruction.

Scoring Rule:  
Assign one score from this set:  
[0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

- 1.0 → Excellent stylistic imitation; rich detail; highly on-topic; fully consistent with persona.  
- 0.0 → Not in character; off-topic; contradicts persona; or stylistically incorrect.  
- Intermediate values reflect partial alignment.

Output Format:  
<score>xx</score>   (Example: <score>0.5</score>)

Now evaluate the following:

=== Instruction ===
{instruction}

=== Ground Truth Writing ===
{ground_truth}

=== Model Writing ===
{model_answer}

Please output only the XML result in <score>xx</score> format.
"""

PERSONA_GEN_PROMPT = """You are an expert evaluator for persona generation.  
You will be given an '=== Instruction ===', a '=== Ground Truth Persona ===', and a '=== Generated Persona ==='.  
Your task is to assess how well the Generated Persona fulfills the requirements described in the Instruction.

Evaluation Criteria:

1. Keyword Faithfulness  
   - Does the persona meaningfully expand the keywords provided in the Instruction?  
   - Are the implied traits, behaviors, and themes captured accurately and deeply?  
   - The persona should not ignore or contradict the keywords.

2. Realism & Psychological Coherence  
   - Does the persona read like a believable human being, with consistent motivations, values, and emotional tendencies?  
   - Does it avoid generic, shallow, or templated descriptions?  
   - The writing should show internal coherence, psychological depth, and a sense of lived experience.

3. Richness & Level of Detail  
   - Is the persona vivid and specific, including concrete elements that make the person feel real (e.g., life events, habits, perspectives, emotional patterns)?  
   - Details do NOT need to match the Ground Truth but should demonstrate a comparable level of richness and narrative depth.  
   - The persona should avoid fabricated contradictions or implausible claims unless supported by the keywords.

4. Compliance With Instructional Constraints  
   - Does the persona fully adhere to the output requirements (e.g., third-person writing, single paragraph, approximate word count)?  
   - Is the tone and structure consistent with a well-formed persona description?

Important Note:  
Do NOT evaluate the Generated Persona based on similarity of meaning or wording to the Ground Truth Persona.  
The Ground Truth is provided only as an example of appropriate depth, realism, and detail density.  
Your evaluation should focus on keyword adherence, realism, richness, and compliance with the formatting instructions.

Scoring Rule:  
Assign one score from the set:  
[0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

- 1.0 → Excellent persona: realistic, richly detailed, faithful to keywords, and compliant with all constraints.  
- 0.0 → Not realistic, ignores keywords, generic, incoherent, or non-compliant.  
- Intermediate scores reflect partial fulfillment of the criteria.

Output Format:  
<score>xx</score>  (Example: <score>0.5</score>)

Now evaluate the following:

=== Instruction ===  
{instruction}

=== Ground Truth Persona ===  
{ground_truth}

=== Generated Persona ===  
{model_answer}

Please output only the XML result in <score>xx</score> format.
"""

# Mapping of evaluation modes to corresponding prompt templates
prompt_map = {
    "social_reasoning": [SOCIAL_REASONING_PROMPT],
    "factual_accuracy": [FACTUAL_ACCURACY_PROMPT],
    "math_problem": [MATH_PROBLEM_PROMPT],
    "tool_usage": [TOOL_USAGE_PROMPT],
    "comprehensive": [COMPREHENSIVE_PROMPT],
    "creative_writing": [CREATIVE_WRITING_PROMPT],
    "semantic_similarity": [SEMANTIC_SIMILARITY_PROMPT],
    "semantic_similarity_keep_think": [SEMANTIC_SIMILARITY_PROMPT_KEEP_THINK],
    "roleplay": [ROLEPLAY_PROMPT],
    "social_r1": [SOCIAL_R1_PROMPT],
    "social_r2": [SOCIAL_R2_PROMPT],
    "social_r3": [SOCIAL_R3_PROMPT],
    "social_r4": [SOCIAL_R4_PROMPT],
    "conversation": [REASONING_REWARD_PROMPT, CONVERSATION_PROMPT],
    "writing": [REASONING_REWARD_PROMPT, PERSONALIZED_WRITING_PROMPT],
    "social_qa": [REASONING_REWARD_PROMPT, SOCIAL_QA_PROMPT],
    "persona": [REASONING_REWARD_PROMPT, PERSONA_GEN_PROMPT],
    "socsci": [REASONING_REWARD_PROMPT],
    "item_selection": [REASONING_REWARD_PROMPT],
    "socialr1": [REASONING_REWARD_PROMPT],
}

# Returns the corresponding prompt template based on the mode
def get_prompt_by_mode(mode="social_reasoning", metric="llm"):
    """Returns the prompt template corresponding to the specified mode
    
    Args:
        mode: Evaluation mode, options include "social_reasoning", "factual_accuracy", "math_problem", 
              "tool_usage", "comprehensive", "creative_writing", "semantic_similarity"
              
    Returns:
        Prompt template string for the corresponding mode
    """
    if metric == "llm":
      return prompt_map[mode][0]
    elif metric == "llm_outcome":
      return prompt_map[mode][1]


if __name__ == "__main__":
    print(SOCIAL_R1_PROMPT)