
# Anthropomorphic Intelligence

**Towards Human-Like AI: The Shaping of Artificial Mind**

---

## Table of Contents

* [Background](#background)
* [Project Goals](#project-goals)
* [Techniques & Sub-Projects](#techniques--sub-projects)
  * [1. PCC: Embedding-based Context Compression](#1-pcc-embedding-based-context-compression)
  * [2. MotiveBench: Benchmarking Human-like Motivation](#2-motivebench-benchmarking-human-like-motivation) 
* [Contributing](#contributing) 
* [Contact](#contact)

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

**SocialCC**  is a novel benchmark designed to evaluate cultural competence through multi-turn interactive intercultural scenarios. It comprises 3,060 human-written scenarios spanning 60 countries across six continents. Through extensive experiments on eight prominent LLMs, our findings reveal a significant gap between the cultural knowledge stored in these models and their ability to apply it effectively in cross-cultural communication.

**Key Features:**
* 3,060 diverse intercultural scenarios spanning 60 countries across six continents.
* Three core evaluation dimensions: cultural awareness, cultural knowledge, and cultural behaviour.
* Interactive multi-turn assessment that measures cultural competence in dynamic, context-rich social interactions.
* Comprehensive cross-model analysis identifying misinterpretation of implicit cultural cues and inconsistent handling of value conflictss.

---

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
