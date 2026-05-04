#!/bin/bash
NGPUS=1
VIDEO_DIR=$HOME/DATA/proactvl/LiveGamingBenchmark/DATA

# livecc-base
CKPT_PATH='oaaoaa/proactvl_base_liveccbase'
BASE_MODEL='chenjoya/LiveCC-7B-Base'
MODEL_ID='proactvl_base_liveccbase'
python -m evaluation.gaming.distributed_generate_gaming --model_name_or_path ${BASE_MODEL} \
    --ckpt_path ${CKPT_PATH} --num_workers ${NGPUS} --model_id ${MODEL_ID} \
    --state_threshold 0.3 \
    --test_name 'streaming_games' \
    --video_dir ${VIDEO_DIR} \
    --output_dir ./results/proactvl/streaming \
    --max_kv_tokens 16384 \
    --dataset_name oaaoaa/LiveGamingBenchmark

python label_streaming2standard.py \
    --ann_path ./results/proactvl/streaming/${MODEL_ID}_30_16384.jsonl \
    --save_path ./results/proactvl/streaming/${MODEL_ID}_30_16384_standard.jsonl --mode pred