#!/bin/bash
NGPUS=2
VIDEO_DIR=$HOME/DATA/proactvl/LiveGamingBenchmark/DATA

# livecc-base
BASE_MODEL='chenjoya/LiveCC-7B-Base'
CKPT_PATH='oaaoaa/proactvl_base_liveccbase'
MODEL_ID='proactvl_base_liveccbase'

python -m evaluation.gaming.distributed_generate_gaming --model_name_or_path ${BASE_MODEL} \
    --ckpt_path ${CKPT_PATH} --num_workers ${NGPUS} --model_id ${MODEL_ID} \
    --state_threshold 0.3 \
    --dataset_name oaaoaa/LiveGamingBenchmark \
    --test_name 'all_in_one' \
    --video_dir ${VIDEO_DIR} \
    --output_dir ./results/proactvl \
    --max_kv_tokens 16384

# qwen2vl
CKPT_PATH='oaaoaa/proactvl_base_qwen2vl'
BASE_MODEL='Qwen/Qwen2-VL-7B-Instruct'
MODEL_ID='proactvl_base_qwen2vl'

python -m evaluation.gaming.distributed_generate_gaming --model_name_or_path ${BASE_MODEL} \
    --ckpt_path ${CKPT_PATH} --num_workers ${NGPUS} --model_id ${MODEL_ID} \
    --state_threshold 0.3 \
    --dataset_name oaaoaa/LiveGamingBenchmark \
    --test_name 'all_in_one' \
    --video_dir ${VIDEO_DIR} \
    --output_dir ./results/proactvl \
    --max_kv_tokens 16384

# qwen2.5vl
CKPT_PATH='oaaoaa/proactvl_base_qwen2_5vl'
BASE_MODEL='Qwen/Qwen2.5-VL-7B-Instruct'
MODEL_ID='proactvl_base_qwen2_5vl'

python -m evaluation.gaming.distributed_generate_gaming --model_name_or_path ${BASE_MODEL} \
    --ckpt_path ${CKPT_PATH} --num_workers ${NGPUS} --model_id ${MODEL_ID} \
    --state_threshold 0.3 \
    --dataset_name oaaoaa/LiveGamingBenchmark \
    --test_name 'all_in_one' \
    --video_dir ${VIDEO_DIR} \
    --output_dir ./results/proactvl \
    --max_kv_tokens 16384

# qwen3vl
CKPT_PATH='oaaoaa/proactvl_base_qwen3vl'
BASE_MODEL='Qwen/Qwen3-VL-8B-Instruct'
MODEL_ID='proactvl_base_qwen3vl'

python -m evaluation.gaming.distributed_generate_gaming --model_name_or_path ${BASE_MODEL} \
    --ckpt_path ${CKPT_PATH} --num_workers ${NGPUS} --model_id ${MODEL_ID} \
    --state_threshold 0.3 \
    --dataset_name oaaoaa/LiveGamingBenchmark \
    --test_name 'all_in_one' \
    --video_dir ${VIDEO_DIR} \
    --output_dir ./results/proactvl \
    --max_kv_tokens 16384