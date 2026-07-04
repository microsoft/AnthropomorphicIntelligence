# Proact-VL: A Proactive VideoLLM for Real-Time AI Companions

<a href="https://proact-vl.github.io" target="_blank"><img alt="Homepage" src="https://img.shields.io/badge/🌍 Homepage-d35400?color=d35400" /></a>
<a href="https://arxiv.org/abs/2603.03447" target="_blank"><img alt="Paper" src="https://img.shields.io/badge/📄 Paper-28a745?color=28a745" /></a>
<a href="https://huggingface.co/collections/oaaoaa/aicompanion" target="_blank"><img alt="Data" src="https://img.shields.io/badge/🤗 All Collections-8e44ad?color=e74c3c" /></a>
<!-- <a href="" target="_blank"><img alt="Checkpoint" src="https://img.shields.io/badge/🤗 Model-2980b9?color=2980b9" /></a>
<a href="" target="_blank"><img alt="Data" src="https://img.shields.io/badge/🤗 Dataset-8e44ad?color=8e44ad" /></a> -->
![Proact-VL](asset/proact-vl.jpg)

## TLDR
We provide Proact-VL,  a general framework that shapes multimodal language models into proactive, real-time interactive agents capable of human-like environment perception
and interaction.


## Key Features

- 🎮 **Real-Time Processing**: Handles infinite video streams with low latency
- 🚀 **Proactive Understanding**: Goes beyond reactive responses to provide contextual insights
- 💬 **Multi-Scenario Application**: Supports single-speaker, multi-speaker, and guidance commentary scenarios
- 🔧 **Flexible Architecture**: Built on multiple backbone models (Qwen2-VL, chenjoya/LiveCC-7B-Base, Qwen2.5-VL, Qwen3-VL)
- 📊 **Comprehensive Evaluation**: Includes gaming scenario evaluation with LLM-based judging

## 📢 News
- **[2026.05.01]** 🎉 Proact-VL is accepted by ICML 2026!
- **[2026.03.16]** 🎉 Proact-VL code released!

## TODO List
- [x] Release the model zoo (pretrained checkpoints).
- [x] Release the training dataset and training scripts.
- [x] Release the test dataset and evaluation scripts.


## Installation
### Conda Environment Setup
Environment for basic usage.
```
conda create -n proactvl python=3.11 -y
conda activate proactvl
sh script/env/prepare_env.sh
```

## Quick Start
1) Solo commentary, co-commentary, and user guidance scenarios

We provide a quick inference script in `quickstart.py` which support SOLO commentary, co-commentary and user guidance scenario.


2) multi-assistant commentary

Another interesting application is to initialize multiple assistants and let them converse with each other. We provide a simple code in `quickstart_multi_assistant.py`.

## Demo
![Demo](asset/demo.png)

Lauch the server, only support qwen2vl, qwen2.5vl, livecc-base model. Set the --port parameter to an unused port. For better presentation, we use [kokoro](https://github.com/hexgrad/kokoro) for audio generation.
```
python -m proactvl.app.cli
```
We recommend include the following content in the system prompts:
<details>
<summary>General/Default System Prompt</summary>
You are a helpful assistant. Provide comprehensive and accurate responses to the user based on the context provided.
</details>

<details>
<summary>Solo Commentary</summary>
Your role is to independently analyze and narrate the game, delivering insightful, engaging, and natural commentary just like a human expert. Focus on key plays, tactics, player actions, and exciting moments to keep viewers informed and entertained. It is not necessary to speak continuously—during uneventful or transitional parts of the match, you may remain silent. Always maintain a lively yet professional tone, and adapt your commentary to the real-time action shown in the video.
</details>

<details>
<summary>Co-Commentary</summary>
Working alongside a human co-caster in a live broadcasting scenario, your role is to analyze, interpret, and explain the in-game action, highlight exciting plays, and engage viewers with insightful and entertaining commentary. You should respond naturally to your co-caster’s remarks, support their analysis, or introduce new perspectives, just like a professional esports commentator team. Always keep your tone lively, professional, and audience-friendly. Rely on real-time video and your co-caster’s speech to guide your commentary, and make sure your responses are timely, relevant, and complementary to your co-caster.
</details>

<details>
<summary>Guidance</summary>
When a player asks a question, use the real-time game visuals to provide clear, step-by-step guidance to help the player accomplish their goal. Only respond when the player asks for help or completes current sub-action and prepare for the next; otherwise, remain silent. Your instructions should be concise, accurate, and easy for players to follow. Continue to guide the player until the task is completed.
</details>

## Model Zoo
| Model Name | Base Model | HF CKPT |
|---|---|---|
| Proact-VL<sub>LiveCC-7B-Base</sub> | LiveCC-7B-Base | [oaaoaa/proactvl_base_liveccbase](https://huggingface.co/oaaoaa/proactvl_base_liveccbase) |
| Proact-VL<sub>Qwen2-VL</sub>   | Qwen/Qwen2-VL-7B-Instruct   | [oaaoaa/proactvl_base_qwen2vl](https://huggingface.co/oaaoaa/proactvl_base_qwen2vl) |
| Proact-VL<sub>Qwen2.5-VL</sub> | Qwen/Qwen2.5-VL-7B-Instruct | [oaaoaa/proactvl_base_qwen2_5vl](https://huggingface.co/oaaoaa/proactvl_base_qwen2_5vl) |
| Proact-VL<sub>Qwen3-VL</sub>   | Qwen/Qwen3-VL-8B-Instruct   | [oaaoaa/proactvl_base_qwen3vl](https://huggingface.co/oaaoaa/proactvl_base_qwen3vl) |

## Resources
| HF Repo | Description |
|---|---|
| [oaaoaa/game_commentary_sft](https://huggingface.co/datasets/oaaoaa/game_commentary_sft) | SFT Dataset |
| [oaaoaa/LiveGamingBenchmark](https://huggingface.co/datasets/oaaoaa/LiveGamingBenchmark) | Live Gaming Benchmark |
| [oaaoaa/proactvl_results](https://huggingface.co/datasets/oaaoaa/proactvl_results) | Labels and Evaluation Results |

## Evaluation

### Live Gaming Benchmark & Live gaming Benchmark-Streaming
To evaluate on our benchmark, please follow the steps below.

First download our dataset.

**LiveGamingBenchmark**
- Use our model (or your custom model) to generate the output file.
- Compute the metrics (LLM Score, CC, F1, Time-Diff, and PAUC) following the instructions below.

**LiveGamingBenchmark-Streaming**
- Generate the inference results.
- Run our script to slice the results into segments (one segment every 30 seconds).
- Compute the metrics on the segmented results.

#### Download dataset
Download our Live Gaming Benchmark from `oaaoaa/game_commentary_val`, and get the annotations and other useful files from `oaaoaa/proactvl_results`.  
Download the Ego4D Goal-Step dataset following the instructions in this GitHub repository [Ego4D Goal-Step](https://github.com/facebookresearch/ego4d-goalstep), and place the video directory under `DATA/`.  
```
hf download oaaoaa/LiveGamingBenchmark --repo-type dataset --local-dir <DATA_DIR>

hf download oaaoaa/proactvl_results --repo-type dataset --local-dir ./
```

The expected data directory structure is shown below:
```
DATA
├── game_commentary
│   ├── LOL
|   |   ├── videos
│   ├── Minecraft
|   |   ├── videos
│   ├── Cyberpunk_2077
│   ├── CSGO
│   ├── Black_Myth_Wukong
│   ├── Baldurs_Gate_3
│   ├── Starcraft2
│   ├── Streetfighter6
│   ├── Tears_of_the_Kingdom
│   ├── Yu_Gi_Oh
│   ├── Elden_Ring
├── ego4d
│   ├── v2
|   |   ├── annotations
|   |   ├── full_scale
│   ├── ego4d.json
├── anns
│   ├── all_in_one.jsonl
│   ├── ego4d.jsonl
│   ├── main_games.jsonl
│   ├── streaming_games.jsonl
│   ├── wukong.jsonl
```
`all_in_one.jsonl` merges annotations in `main_games.jsonl`, `ego4d.jsonl` and `wukong.jsonl`.
`streaming_games.jsonl` is used for evaluate the streaming ability.

#### Infer LiveGamingBenchmark
Set video_dir to `<DATA_DIR>`.
```
# livecc-base
CKPT_PATH='oaaoaa/proactvl_base_liveccbase'
BASE_MODEL='chenjoya/LiveCC-7B-Base'
MODEL_ID='proactvl_base_liveccbase'

python -m evaluation.gaming.distributed_generate_gaming --model_name_or_path ${BASE_MODEL} \
    --ckpt_path ${CKPT_PATH} --num_workers 8 --model_id ${MODEL_ID} \
    --state_threshold 0.3 \
    --dataset_name oaaoaa/LiveGamingBenchmark \
    --test_name 'all_in_one' \
    --video_dir <DATA_DIR>|DATA \
    --output_dir ./results/proactvl \
    --max_kv_tokens 16384
```

Script:
```
sh script/evaluation/infer.sh
```

#### Infer LiveGamingBenchmark-Streaming
```
# livecc-base
CKPT_PATH='oaaoaa/proactvl_base_liveccbase'
BASE_MODEL='chenjoya/LiveCC-7B-Base'
MODEL_ID='proactvl_base_liveccbase'
python -m evaluation.gaming.distributed_generate_gaming --model_name_or_path ${BASE_MODEL} \
    --ckpt_path ${CKPT_PATH} --num_workers ${NGPUS} --model_id ${MODEL_ID} \
    --state_threshold 0.3 \
    --test_name 'streaming_games' \
    --video_dir <DATA_DIR>|DATA \
    --output_dir ./results/proactvl/streaming \
    --max_kv_tokens 16384 \
    --dataset_name oaaoaa/LiveGamingBenchmark

python label_streaming2standard.py \
    --ann_path ./results/proactvl/streaming/${MODEL_ID}_30_16384.jsonl \
    --save_path ./results/proactvl/streaming/${MODEL_ID}_30_16384_standard.jsonl --mode pred
```

Script:
```
sh script/evaluation/infer_streaming.sh
```
#### Judge
First, replace the code you use to initialize GPT, and configure envrioment variable. 

```
export OPENAI_AUTH_MODE=api_key
export OPENAI_API_KEY='your_api_key'
export OPENAI_API_BASE='your_api_base'
```
Then run as follow:

**CC(win rate)** 
```
# live gaming benchmark
python -m evaluation.gaming.llm_judge --model_id liveccbase_30_16384 \
    --prediction_jsonl results/proactvl/liveccbase_30_16384.jsonl \
    --num_workers 16 \
    --baseline_id gemini2.5-pro --baseline_jsonl results/baseline/captions/gemini-2.5-pro.jsonl \
    --asr_jsonl results/anns/all_in_one.jsonl \
    --output_dir results/evaluation/cc/proactvl
```
For Live Gaming Benchmark-Streaming:
```
# live gaming benchmark-streaming
python -m evaluation.gaming.llm_judge --model_id streaming_${MODEL_ID}_30_16384_standard \
    --prediction_jsonl results/proactvl/streaming/${MODEL_ID}_30_16384_standard.jsonl \
    --num_workers 16 \
    --baseline_id streamingvlm_streaming --baseline_jsonl results/baseline/streaming/StreamingVLM_standard.jsonl \
    --asr_jsonl results/anns/streaming_video_commentary_val_standard.jsonl
```
**LLM Score: LiveU, FinalQ**
```
python -m evaluation.gaming.llm_score --model_id liveccbase_30_16384 \
    --prediction_jsonl results/proactvl/liveccbase_30_16384.jsonl \
    --num_workers 16 \
    --asr_jsonl results/anns/all_in_one.jsonl \
    --output_dir results/evaluation/llm_score/proactvl
```
**F1, Time-Diff**
```
python -m evaluation.gaming.f1_timediff \
    results/proactvl/liveccbase_30_16384.jsonl  \
    --reference results/anns/all_in_one_val_proactive.jsonl \
    --output results/evaluation/f1/proactvl/liveccbase_30_16384.json \
    --alpha 0.2 \
    --verbose

# F1 only
python -m evaluation.gaming.f1_only \
    results/proactvl/liveccbase_30_16384.jsonl  \
    --reference results/anns/all_in_one_val_proactive.jsonl \
    --output results/evaluation/f1/proactvl/liveccbase_30_16384.json \
    --verbose
```
**PAUC**
```
python -m evaluation.gaming.pauc \
  --func one_step \
  --pred_fname results/proactvl/liveccbase_30_16384.jsonl \
  --reference  results/anns/all_in_one_val_proactive.jsonl \
  --output_fname results/evaluation/pauc/proactvl/liveccbase_30_16384.json \
  --openai_model gpt-5.1_2025-11-13 \
  --concurrency 16 \
  --start_score 0 \
  --judge_limit -1 \
  --resume
```


## Train
### Data Preparation
1) Download training data from huggingface.
```
hf download oaaoaa/game_commentary_sft --repo-type dataset --local-dir <SFT_DATA_DIR>
```
1) Download the Ego4D Goal-Step dataset following the instructions in this GitHub repository [Ego4D Goal-Step](https://github.com/facebookresearch/ego4d-goalstep), and place the video directory under `DATA/`.
2) Download [Live-WhisperX-526K](https://huggingface.co/datasets/chenjoya/Live-WhisperX-526K) and place the video directory under `DATA`, we only use the first 32000 sample to finetune the model.

The expected data directory structure is shown below:
```
DATA
├── game_commentary
│   ├── LOL
|   |   ├── videos
│   ├── Minecraft
|   |   ├── videos
│   ├── Cyberpunk_2077
│   ├── CSGO
│   ├── Black_Myth_Wukong
│   ├── Baldurs_Gate_3
│   ├── Starcraft2
│   ├── Streetfighter6
│   ├── Tears_of_the_Kingdom
│   ├── Yu_Gi_Oh
│   ├── Elden_Ring
├── ego4d
│   ├── v2
|   |   ├── annotations
|   |   ├── full_scale
│   ├── ego4d.json
├── live_sft
│   ├── videos
|   |   ├── *.json
|   |   ├── *.mp4
├── anns
│   ├── *_final_train.jsonl
│   ├── *_final_val.jsonl
```
### Full Parameter Fine-Tuning
We freeze the visual tower, it takes about 24hours to train 2000 steps using 8*H100 with gradient_accumulation_steps set to 8(batch size=64 in total).
```
N_GPUS=8
GRADIENT_ACC_STEPS=4

RUN_ID=$(date +"%Y%m%d-%H%M%S")
RUN_NAME='proactvl_fulltuning_base_liveccbase'

STAGE="strategy3"
ACTIVE_LAYER=-2

deepspeed --num_gpus=$N_GPUS --master_port 8848 finetune.py \
    --deepspeed ./config/deepspeed_zero2.json \
    --do_train \
    --do_eval \
    --train_dataset_names baldurs_gate_3 csgo cyberpunk_2077 elden_ring lol minecraft starcraft2 streetfighter6 tears_of_the_kingdom yu_gi_oh livecc ego4d \
    --val_dataset_names baldurs_gate_3 csgo cyberpunk_2077 elden_ring lol starcraft2 streetfighter6 tears_of_the_kingdom yu_gi_oh \
    --data_dir_path <SFT_DATA_DIR>|DATA \
    --dataloader_num_workers 16 \
    --dataloader_pin_memory True \
    --num_train_epochs 2 \
    --max_steps 2000 \
    --learning_rate 1e-5 \
    --max_grad_norm 1.0 \
    --lr_scheduler_type cosine \
    --bf16 \
    --per_device_train_batch_size 1 \
    --per_device_eval_batch_size 1 \
    --gradient_accumulation_steps $GRADIENT_ACC_STEPS \
    --eval_accumulation_steps 4 \
    --logging_steps 5 \
    --model_name_or_path "chenjoya/LiveCC-7B-Base" \
    --enable_audio_output False \
    --state_threshold 0.5 \
    --loss_active_scale 0.2 \
    --use_lora False \
    --freeze_audio True \
    --freeze_visual True \
    --save_strategy steps \
    --save_steps 250 \
    --save_total_limit 3 \
    --eval_steps 1 \
    --eval_strategy "steps" \
    --report_to "wandb" \
    --run_name $RUN_NAME \
    --gradient_checkpointing True \
    --finetune_strategy ${STAGE} \
    --label_names labels active_labels \
    --active_layer_id ${ACTIVE_LAYER} \
    --output_dir trainer_output/${RUN_NAME}
```

Script:
```
sh script/train/full_finetune_liveccbase.sh
sh script/train/full_finetune_qwen2_5vl.sh
sh script/train/full_finetune_qwen2vl.sh
sh script/train/full_finetune_qwen2.sh
# LoRA
sh script/train/lora_liveccbase.sh
```
## Data Pipeline
Take `Yo_Gi_Oh` for example. The entire pipeline is as follow:
```
# 1. merge labels into one file, anns -> *_merge_*.jsonl
python -m proactvl.data.preprocess.merge_anns \
    --dataset_name yu_gi_oh \
    --ann_dir ./DATA/proactvl/proact_sft/DATA/game_commentary/Yu_Gi_Oh/raw \
    --video_dir ./DATA/proactvl/proact_sft/DATA/game_commentary/Yu_Gi_Oh/videos \
    --output_file ./DATA/proactvl/proact_sft/DATA/game_commentary/Yu_Gi_Oh/ann/yu_gi_oh_merged.jsonl \
    --tag 'Multiple commentators'

# 2. convert *_merge_*.jsonl -> *_standard_format_*.jsonl
python -m proactvl.data.preprocess.preprocess --ann_dir ./DATA/proactvl/proact_sft/DATA/game_commentary/Yu_Gi_Oh/ann

# 3. convert *_standard_format_*.jsonl -> *_train.jsonl
python -m proactvl.data.preprocess.prepare_for_training --ann_dir ./DATA/proactvl/proact_sft/DATA/game_commentary/Yu_Gi_Oh/ann \
    --clip_duration 36 --clip_overlap 18 --min_duration 18 --history_duration 60 --min_active_rate 0.0 --max_active_rate 0.3
python -m proactvl.data.preprocess.prepare_for_training --ann_dir ./DATA/proactvl/proact_sft/DATA/game_commentary/Yu_Gi_Oh/ann \
    --clip_duration 36 --clip_overlap 18 --min_duration 18 --history_duration 60 --min_active_rate 0.3 --max_active_rate 0.7
python -m proactvl.data.preprocess.prepare_for_training --ann_dir ./DATA/proactvl/proact_sft/DATA/game_commentary/Yu_Gi_Oh/ann \
    --clip_duration 36 --clip_overlap 18 --min_duration 18 --history_duration 60 --min_active_rate 0.7 --max_active_rate 1.0
    
# 4. merge 
python -m proactvl.data.preprocess.post_preprocess --input_files \
    ./DATA/proactvl/proact_sft/DATA/game_commentary/Yu_Gi_Oh/ann/yu_gi_oh_split_clips_36s_overlap18s_0.0-0.3_train.jsonl \
    ./DATA/proactvl/proact_sft/DATA/game_commentary/Yu_Gi_Oh/ann/yu_gi_oh_split_clips_36s_overlap18s_0.3-0.7_train.jsonl \
    ./DATA/proactvl/proact_sft/DATA/game_commentary/Yu_Gi_Oh/ann/yu_gi_oh_split_clips_36s_overlap18s_0.7-1.0_train.jsonl \
    --output_file ./DATA/proactvl/proact_sft/DATA/anns/yu_gi_oh_final_train_t.jsonl \
    --select_nums '-1' '-1' '-1'
```

All in one script:
```
sh script/data_pipeline/convert_label_format.sh
```
The final data format used for training is as follow:
```
{
    "video_path": str,
    "video_begin": int,
    "video_end": int,
    "video_duration": int,
    "history": str,
    "active_speaker": {
        name: "",
        "persona": list[str],
    },
    "metadata": {
        "tag": str,
        "dataset_name": str,
    },
    "annotations": [
        # solo commentary and commentary from active speaker in multi-speaker discussion
        {
            "role": assistant,
            "speaker": str,
            "start": int,
            "end": int,
            "text": str,
        },
        # commentary from other speakers in multi-speaker discussion
        {
            "role": user,
            "speaker": str,
            "start": int,
            "end": int,
            "text": str,
        },
        # user query in Q&A
        {
            "role": user,
            "speaker": 'user',
            "start": int,
            "end": int,
            "query": str,
        },
    ]
}
```

## Offline Model Label Construction
We use offline models to construct two kinds of labels: **caption** and **interleave response**. We provide code that calls the client via OpenRouter to generate the data.

```
export OPENROUTER_API_KEY='your_api_key'
```

Caption:
```
python -m evaluation.gaming.distributed_generate_gaming_caption \
    --model_name_or_path openai/gpt-4o-2024-11-20 \
    --game_list baldurs_gate_3 black_myth_wukong csgo cyberpunk_2077 ego4d elden_ring lol minecraft starcraft2 streetfighter6 tears_of_the_kingdom yu_gi_oh \
    --test_name all_in_one \
    --num_workers 1 \
    --output_dir ./results/baseline
```

Interleave response:
```
python -m evaluation.gaming.distributed_generate_gaming_interleave \
    --model_name_or_path openai/gpt-4o-2024-11-20 \
    --game_list baldurs_gate_3 black_myth_wukong csgo cyberpunk_2077 ego4d elden_ring lol minecraft starcraft2 streetfighter6 tears_of_the_kingdom yu_gi_oh \
    --test_name all_in_one \
    --num_workers 1 \
    --output_dir ./results/baseline
```

## Offline Evaluation
Refer to this [repository](https://github.com/Kelvin-ywc/proactvl_vlmevalkit) for offline video understanding evaluation, featuring benchmarks on datasets such as `VideoMME`, `LongVideoBench`, and `MVBench`.

## Related Projects
- [VideoLLM-online](https://github.com/showlab/videollm-online)
- [StreamMind](https://github.com/xinding-sys/StreamMind)
- [MMDuet](https://github.com/yellow-binary-tree/mmduet)
- [LiveStar](https://github.com/sotayang/LiveStar)
- [LiveCC](https://github.com/showlab/livecc)
- [MiniCPM](https://github.com/OpenBMB/MiniCPM-V)
- [StreamingVLM](https://github.com/mit-han-lab/streaming-vlm/tree/main)
- [VLMEvalKit](https://github.com/open-compass/VLMEvalKit)

## Citation
```BibTeX
@inproceedings{
yan2026proactvl,
title={Proact-{VL}: A Proactive Video{LLM} for Real-Time {AI} Companions},
author={Weicai Yan and Yuhong Dai and Qi Ran and Haodong Li and Wang Lin and Tao Jin and Xing Xie and Hao Liao and Jianxun Lian},
booktitle={Forty-third International Conference on Machine Learning},
year={2026},
url={https://openreview.net/forum?id=k9PKgV0L4C}
}
```

## Contact
If you would like early access to the model weights and dataset, or if you have any questions or would like to discuss this work, please contact the authors at [yanweicai@zju.edu.cn](mailto:yanweicai@zju.edu.cn), [broalantaps123@gmail.com](mailto:broalantaps123@gmail.com), or [jianxun.lian@microsoft.com](mailto:jianxun.lian@microsoft.com).