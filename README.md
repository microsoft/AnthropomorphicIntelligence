
# Anthropomorphic Intelligence

**Towards Human-Like AI: The Shaping of Artificial Mind**

---

## Table of Contents

- [Anthropomorphic Intelligence](#anthropomorphic-intelligence)
  - [Table of Contents](#table-of-contents)
  - [Background](#background)
  - [Project Goals](#project-goals)
  - [Techniques \& Sub-Projects](#techniques--sub-projects)
    - [1. PCC: Embedding-based Context Compression](#1-pcc-embedding-based-context-compression)
    - [2. MotiveBench: Benchmarking Human-like Motivation](#2-motivebench-benchmarking-human-like-motivation)
    - [3. SocialCC: Interactive Evaluation for Cultural Competence in Language Agents](#3-socialcc-interactive-evaluation-for-cultural-competence-in-language-agents)
    - [4. LearnArena: Benchmarking Learning Ability](#4-learnarena-benchmarking-learning-ability)
    - [5. PersonaArena: Role-Play Simulation and Evaluation](#5-personaarena-role-play-simulation-and-evaluation)
    - [6. HumanLLM: Towards Personalized Understanding and Simulation of Human Nature](#6-humanllm-towards-personalized-understanding-and-simulation-of-human-nature)
    - [7. Proact-VL: A Proactive VideoLLM for Real-Time AI Companions](#7-proact-vl-a-proactive-videollm-for-real-time-ai-companions)
    - [8. Social-R1: Towards Human-like Social Reasoning in LLMs](#8-social-r1-towards-human-like-social-reasoning-in-llms)
  - [Contributing](#contributing)
  - [Trademarks](#trademarks)
  - [Privacy](#privacy)
  - [Contact](#contact)

---

## Background

Recent years have witnessed remarkable advancements in AI’s ability to perform objective tasks—ranging from mathematics and coding to various forms of logical reasoning. However, as we approach a society of human-AI symbiosis, crucial dimensions of human-like cognition, ideology, and consciousness—essential for rich, meaningful human-AI interactions—have remained underexplored.

Looking forward, AI agents that can understand, empathize with, and support users—much like close family and friends—will increasingly deliver value across business and societal domains. Companion-like AI systems that offer emotional support, proactive engagement, and personalized experiences have the potential to act as digital humans in diverse scenarios, such as AI non-player characters (NPCs), Social companions, Virtual Tubers, Digital colleagues, Personal coaching, Large-scale societal simulations.

---

## Project Goals

Unlike efforts focused on super-intelligent AI, this project centers on **evaluating and promoting anthropomorphic intelligence**—AI agents with a human-like mindset and a degree of awareness, capable of acting proactively and autonomously. Our goals are to:

* Equip AI agents with cognitive traits and social reasoning capacities inspired by humans.
* Enable rich, sustained social interactions and collaboration between AI agents, humans, and other AI agents.
* Provide personalized, human-preferred services in business and societal domains.

This repository gathers and develops various techniques that contribute toward these objectives.

---

## Techniques & Sub-Projects

### 1. [PCC: Embedding-based Context Compression](./PCC/README.md)

**PCC** is a technique inspired by human cognitive patterns, aiming to enable large language models (LLMs) to efficiently process long contexts by converting context signals into compact, dense representations. This decoupled compressor-LLM framework leverages embedding-based context compression to significantly reduce inference costs while maintaining essential contextual information and accuracy. Thorough pretraining and adaptive compression rates allow PCC to improve LLM efficiency across various tasks, models, and domains—making it well-suited for real-world applications, especially in resource-constrained environments.

**Key Features:**

* Embedding-based condensed compression for efficiency
* Decoupled compressor-LLM architecture with downstream LLM untouched 
* Adaptability to various LLMs and downstream tasks

---

### 2. [MotiveBench: Benchmarking Human-like Motivation](./MotiveBench/README.md)

**MotiveBench** is a comprehensive benchmark designed to evaluate and advance the ability of AI agents to demonstrate human-like motivations and proactive behaviors. By presenting 200 rich contextual scenarios and 600 reasoning tasks across multiple motivational levels—including emotional, social, and practical drivers—MotiveBench rigorously tests whether LLMs can autonomously identify and pursue meaningful actions, not just respond reactively. Analysis across multiple popular model families reveals key challenges, such as reasoning about “love & belonging” motivations, and highlights the current gap between AI and true human-like motivational reasoning.

**Key Features:**

* 200 rich contextual scenarios and 600 reasoning tasks
* Multiple levels of motivation, including motivation reasoning, behavior reasoning, and behavior prediction.
* Cross-model benchmarking and insights

---


### 3. [SocialCC: Interactive Evaluation for Cultural Competence in Language Agents](./SocialCC/README.md)



**SocialCC** is a novel benchmark designed to evaluate cultural competence through multi-turn interactive intercultural scenarios. It comprises 3,060 human-written scenarios spanning 60 countries across six continents. Through extensive experiments on eight prominent LLMs, our findings reveal a significant gap between the cultural knowledge stored in these models and their ability to apply it effectively in cross-cultural communication.

**Key Features:**

- 3,060 diverse intercultural scenarios spanning 60 countries across six continents.
- Three core evaluation dimensions: cultural awareness, cultural knowledge, and cultural behaviour.
- Interactive multi-turn assessment that measures cultural competence in dynamic, context-rich social interactions.
- Comprehensive cross-model analysis identifying misinterpretation of implicit cultural cues and inconsistent handling of value conflictss.

------

### 4. [LearnArena: Benchmarking Learning Ability](./LearnArena/README.md)

**LearnArena** is a cognitively grounded benchmark for assessing how LLMs **learn**—not just solve static tasks—across three dimensions: **Learning from Instructor** (interactive feedback), **Learning from Concept** (rule summaries), and **Learning from Experience** (self-selected trajectory reuse). Built on a modified TextArena setup, it standardizes a two-player loop where the evaluated model plays 20 matches per environment, receives teacher feedback, conditions on concise rules, and leverages prior games as in-context examples.

**Key Features:**

- Three learning dimensions: instructor feedback (LfI), concept summaries (LfC), experience trajectories (LfE)
- Unified protocol: 8 environments, 20 matches per model, fixed teacher opponent, win-rate metric
- Cross-model benchmarking and insights on scale limits, instructor quality, and few- vs. many-shot behavior

---

### 5. [PersonaArena: Role-Play Simulation and Evaluation](./PersonaArena/README.md)

**PersonaArena** is a dynamic simulation framework for evaluating persona-level role-playing in LLMs. It builds persona-grounded social scenes, runs multi-turn interactions among a narrator, a protagonist model, and NPCs, and records full action–dialogue trajectories. A multi-agent debating judge then evaluates persona fidelity, coherence, and adaptability, producing detailed and aggregated metrics that support rigorous comparison and improvement.

**Key Features:**

- A persona-grounded social simulation framework that elicits behaviors via dynamic, multi-turn interactions
- A multi-agent debating judge for holistic and unbiased evaluation of role-playing quality
- Elicited data that can be used for targeted post-training to improve persona consistency and realism

---

### 6. [HumanLLM: Towards Personalized Understanding and Simulation of Human Nature](./HumanLLM/README.md)

**HumanLLM** is a human-centric foundation model designed to enable large language models to understand and simulate individual human behaviors, cognition, and preferences. Built upon the Cognitive Genome Dataset, which aggregates millions of real-world user records from platforms such as Reddit, Twitter, Blogger, and Amazon, HumanLLM learns the relationship between a person’s identity, their environment, and resulting actions. Through a diverse set of training tasks—covering persona understanding, social reasoning, and personalized generation—the model is trained to predict user actions and inner thoughts, mimic user writing styles and preferences, and generate authentic user profiles. Extensive evaluations across in-domain tasks and out-of-domain social intelligence benchmarks demonstrate that HumanLLM significantly improves models’ ability to model human behavior and generate realistic, personalized responses. 

**Key Features:**

* A large-scale Cognitive Genome Dataset constructed from real-world user records across multiple platforms, supported by a rigorous multi-stage pipeline including data filtering, data synthesis, and automated quality control to produce high-quality behavior logs for training.

* A model-agnostic multi-task training paradigm that enhances LLMs’ social intelligence through diverse tasks, including profile generation, scenario generation, social question answering, writing imitation, personalized commenting, and preference prediction.

* HumanLLM achieves superior performance in predicting user actions and inner thoughts, more accurately mimics user writing styles and preferences, and generates more authentic user profiles compared to base models. Furthermore, it shows significant gains on out-of-domain social intelligence benchmarks such as MotiveBench and ToMBench, indicating enhanced generalization.

---

### 7. [Proact-VL: A Proactive VideoLLM for Real-Time AI Companions](./Proact-VL/README.md)
**Proact-VL** is a general framework that shapes multimodal language models into proactive, real-time interactive agents capable of human-like environment perception and interaction. It is built on multiple backbone models (Qwen2-VL, Qwen2.5-VL, Qwen3-VL) and supports solo commentary, co-commentary, and user guidance scenarios.

**Key Features:**
- **Real-Time Processing**: Handles infinite video streams with low latency
- **Multi-Modal Commentary**: Supports single-speaker, multi-speaker, and guidance commentary scenarios
- **Proactive Understanding**: Goes beyond reactive responses to provide contextual insights
- **Flexible Architecture**: Built on multiple backbone models (Qwen2-VL, Qwen2.5-VL, Qwen3-VL)
- **Comprehensive Evaluation**: Includes gaming scenario evaluation with LLM-based judging

---

### 8. [Social-R1: Enhancing Social Reasoning in LLMs through Trajectory-Level Reinforcement Learning](https://github.com/jincenziwu/SocialR1)

**Social-R1** is a reinforcement learning framework that aligns LLM reasoning at the trajectory level for human-like social reasoning. It identifies two core failure modes—**Reasoning Parasitism** (models prematurely anchor on answer options and construct post-hoc justifications) and the **Interpretation Bottleneck** (models fail to map social cues to latent mental states)—and addresses them through multi-dimensional rewards inspired by Social Information Processing (SIP) theory. Combined with **ToMBench-Hard**, a challenging Theory-of-Mind dataset with 800 expert-annotated adversarial questions, Social-R1 enables smaller models to match or outperform substantially larger baselines across static, generative, and interactive evaluation settings.

**Key Features:**

* ToMBench-Hard Benchmark: 800 expert-annotated adversarial questions covering six Theory-of-Mind dimensions
* Multi-dimensional reward system with SIP structural reward, SIP content reward, inference efficiency, and curriculum-style weighting
* SIP-guided reasoning enforcing stage-consistent social inference (Cue Encoding → Cue Interpretation → Goal Clarification → Response Generation) 
* Cross-family generalisation across Qwen3-4B, Qwen3-8B, and Llama-3.1-8B-Instruct
* Comprehensive evaluation across static MCQ (8 benchmarks), open-ended generation (FanToM), and interactive social intelligence (SOTOPIA)

## Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.opensource.microsoft.com.

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

---

## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft 
trademarks or logos is subject to and must follow 
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.
Any use of third-party trademarks or logos are subject to those third-party's policies.

---

## Privacy

[Microsoft Privacy Statement](https://go.microsoft.com/fwlink/?LinkId=521839).

---

## Contact

For questions, suggestions, or collaborations, please contact:
\[jianxun.lian@microsoft.com]
\[deeprec@microsoft.com]
