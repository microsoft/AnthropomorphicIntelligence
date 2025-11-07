# SocialCC
## Project Description 

This is the official repository for our paper *"SocialCC: Interactive Evaluation for Cultural Competence in Language Agents"*

![venue](https://img.shields.io/badge/Venue-ACL--25-278ea5) [![Paper PDF](https://img.shields.io/badge/Paper-PDF-yellow.svg)](https://aclanthology.org/2025.acl-long.1594.pdf)

![](pic/SocialCCFramework.png)



## Usage Guide
### Dependencies
To set up the required environment, run:
```
bash build_environment.sh
conda activate socialcc
```
This script installs all necessary Python modules and dependencies.

### Evaluation Pipeline
#### Step 1: Set up Ollama & Start Ollam serve 
```
curl -fsSL https://ollama.com/install.sh | sh
ollama serve
```
#### Step 2: Pull and run closed models (in another terminal) 
```
ollama pull llama2:7b-chat
```
Pulling model llama2:7b-chat will download the required files for evaluation.

#### Step 3: Evaluation sepcifict LLMs 
Choose one of the following:
##### (a) Open Model 
```
bash run_open_model.sh
```
##### (b) Closed Model 
```
bash run_closed_model.sh
```
You can modify the .sh file to select Microsoft Entra ID-based authentication or API key authentication.
To update your credentials, change the authentication setting in gen_closed_model_azure for Entra ID-based authentication, or update the API keys in model_config_agent1.json and model_config_agent2.json.


##### Step 4. Check Final Result in result file
All evaluation results are saved automatically.
You can find the final output files in the result directory.
