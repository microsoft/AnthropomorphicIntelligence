#!/bin/bash
set -e   

echo Setting Environment

# 获取当前脚本所在目录
SCRIPT_DIR="$(dirname "$0")"

# 使用当前目录下的 environment.yml
conda env create -f "${SCRIPT_DIR}/environment.yml"

conda init
source ~/.bashrc
conda activate socialcc


