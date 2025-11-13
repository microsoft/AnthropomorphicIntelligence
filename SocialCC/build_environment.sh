#!/bin/bash
set -e   

echo Setting Environment


SCRIPT_DIR="$(dirname "$0")"


conda env create -f "${SCRIPT_DIR}/environment.yml"

conda init
source ~/.bashrc
conda activate socialcc
 

