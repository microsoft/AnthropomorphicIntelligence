#!/bin/bash

# Initialize submodules script for SocialR1_Code
eval "$(conda shell.bash hook)"

SCRIPT_DIR=$(cd "$(dirname "$0")"; pwd)
PROJECT_DIR=$(realpath "${SCRIPT_DIR}/../..")
SUBMODULES_DIR="${PROJECT_DIR}/submodules"

echo "========= SocialR1_Code Submodules Initialization ========="
echo "Project dir: ${PROJECT_DIR}"

# 1. Initialize verl
echo ">>> Setting up verl environment"
conda create -n verl python=3.10 -y
conda activate verl
cd "$SUBMODULES_DIR/verl"
pip install -e ".[vllm]"
pip install datasets
pip install faiss-gpu
pip install FlagEmbedding
pip install duckdb
pip install mem0ai
pip install "numpy<2"
pip install sandbox_fusion json_repair ollama mathruler tensordict omegaconf
pip install flask
pip install -r $SUBMODULES_DIR/verl/requirements_sglang.txt
pip install https://github.com/Dao-AILab/flash-attention/releases/download/v2.8.0.post2/flash_attn-2.8.0.post2+cu12torch2.5cxx11abiFALSE-cp310-cp310-linux_x86_64.whl
echo ">>> verl setup complete"

echo "========= All submodules initialized successfully! ========="
echo "Available conda environments:"
echo "- verl: For verl library"
echo ""
echo "To activate an environment, use: conda activate <env_name>"
