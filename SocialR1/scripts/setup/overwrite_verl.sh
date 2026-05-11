#!/bin/bash
SCRIPT_DIR=$(cd "$(dirname "$0")"; pwd)
PROJECT_DIR=$(realpath "${SCRIPT_DIR}/../..")

SRC="${PROJECT_DIR}/verl_overwrite"
DST="${PROJECT_DIR}/submodules/verl"

cp -r ${SRC}/reward_score/* ${DST}/verl/utils/reward_score/

cp -r ${SRC}/grpo_trainer/* ${DST}/examples/grpo_trainer

cp -r ${SRC}/dataset/* ${DST}/verl/utils/dataset/

cp -r ${SRC}/fs.py ${DST}/verl/utils/fs.py

cp -r ${SRC}/ray_trainer.py ${DST}/verl/trainer/ppo/ray_trainer.py

cp -r ${SRC}/naive.py ${DST}/verl/workers/reward_manager/naive.py
