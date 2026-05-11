#!/bin/bash
SCRIPT_DIR=$(cd "$(dirname "$0")"; pwd)
PROJECT_DIR=$(realpath "${SCRIPT_DIR}/../..")

export OPENAI_API_MODEL="gpt-4o"
export OPENAI_API_TYPE="openai"
python ${PROJECT_DIR}/submodules/verl/verl/utils/reward_score/AsyncInference/server.py --port 8134
