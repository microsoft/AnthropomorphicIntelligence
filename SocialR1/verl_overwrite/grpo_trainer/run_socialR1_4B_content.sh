#!/bin/bash

# ================= Dynamic Path Configuration =================
# Get the directory where the current script is located: 
# Expected: .../Code/LLMtoolkits/submodules/verl/examples/grpo_trainer
SCRIPT_DIR=$(cd "$(dirname "$0")"; pwd)

# Move up 5 levels to reach the 'Code' root directory, then navigate to 'Data/Train'
# Path Trace: grpo_trainer(0) -> examples(1) -> verl(2) -> submodules(3) -> LLMtoolkits(4) -> Code(5)
DATA_DIR=$(realpath "${SCRIPT_DIR}/../../../../dataset")

# Check if the data directory exists
if [ ! -d "$DATA_DIR" ]; then
    echo "Error: Data directory not found at $DATA_DIR"
    exit 1
fi
# ==============================================================

export VLLM_ATTENTION_BACKEND=XFORMERS
log_path="$(realpath "${SCRIPT_DIR}/../../../../outputs")/Log_SocialR14B"
mkdir -p $log_path

export NCCL_DEBUG=INFO
export NCCL_P2P_DISABLE=1
export CUDA_DEVICE_ORDER=PCI_BUS_ID

export BASE_MODEL='Qwen/Qwen3-4B'

# Define dataset paths using the dynamically calculated relative path
train_datasets="[${DATA_DIR}/SocialRL_Train_V2_SocialR2.parquet]"
test_datasets="[${DATA_DIR}/SocialRL_Test_V2_SocialR2.parquet]"

echo "Script Directory: $SCRIPT_DIR"
echo "Calculated Data Directory: $DATA_DIR"
echo "Train Datasets: $train_datasets"
echo "Test Datasets: $test_datasets"

nproc_per_gpu=16 
nnodes=1
ngpu_per_node=4
total_procs=$(( nproc_per_gpu * nnodes * ngpu_per_node ))
mini_batch_size=$(( total_procs ))

BEIJING_TIME=$(TZ="Asia/Shanghai" date "+%m%d_%H%M")

export WANDB_DIR='SocialR1_4B'
export WANDB_Name='SocialR1_4B'
export WANDB_PROJECT=${WANDB_DIR}
export WANDB_API_KEY=' '
export HYDRA_FULL_ERROR=1
export CUDA_LAUNCH_BLOCKING=1
export WANDB_MODE="online"
export WANDB_EXP="Qwen3-4B+GRPO+RM_V4_Len_Struc_01"
export WANDB_RUN_ID=$WANDB_EXP

echo "Using experiment name: $WANDB_EXP with Beijing time: $BEIJING_TIME"

# Note: Maintaining original 'cd' logic. 
# If the outputs directory structure changes, it is recommended to use relative paths here as well.
PROJECT_DIR=$(realpath "${SCRIPT_DIR}/../../../../")
cd ${PROJECT_DIR}/outputs
export PYTHONPATH=${PROJECT_DIR}/submodules/verl:$PYTHONPATH
export SAVE_DATA=false

python3 -m verl.trainer.main_ppo \
    algorithm.adv_estimator=grpo \
    data.train_files=$train_datasets \
    data.val_files=$test_datasets \
    data.train_batch_size=64 \
    data.max_prompt_length=1024 \
    data.max_response_length=3072 \
    actor_rollout_ref.rollout.max_num_batched_tokens=4096 \
    data.filter_overlong_prompts=True \
    data.truncation='error' \
    actor_rollout_ref.model.path=$BASE_MODEL \
    actor_rollout_ref.actor.optim.lr=1e-6 \
    actor_rollout_ref.model.use_remove_padding=True \
    actor_rollout_ref.actor.ppo_mini_batch_size=16 \
    actor_rollout_ref.actor.ppo_micro_batch_size_per_gpu=1 \
    actor_rollout_ref.actor.use_kl_loss=True \
    actor_rollout_ref.actor.kl_loss_coef=0.001 \
    actor_rollout_ref.actor.kl_loss_type=low_var_kl \
    actor_rollout_ref.actor.entropy_coeff=0 \
    actor_rollout_ref.model.enable_gradient_checkpointing=True \
    actor_rollout_ref.actor.fsdp_config.param_offload=True \
    actor_rollout_ref.actor.fsdp_config.optimizer_offload=True \
    actor_rollout_ref.rollout.log_prob_micro_batch_size_per_gpu=4 \
    actor_rollout_ref.rollout.tensor_model_parallel_size=4 \
    actor_rollout_ref.rollout.name=vllm \
    actor_rollout_ref.rollout.gpu_memory_utilization=0.4 \
    actor_rollout_ref.rollout.n=5 \
    actor_rollout_ref.ref.log_prob_micro_batch_size_per_gpu=4 \
    actor_rollout_ref.ref.fsdp_config.param_offload=True \
    algorithm.use_kl_in_reward=False \
    trainer.critic_warmup=0 \
    trainer.logger='["console","wandb"]' \
    trainer.n_gpus_per_node=4 \
    trainer.nnodes=1 \
    trainer.project_name=${WANDB_PROJECT} \
    trainer.experiment_name=${WANDB_EXP} \
    trainer.save_freq=30 \
    trainer.total_epochs=30 \
    trainer.test_freq=5 \
    trainer.val_before_train=True \
    actor_rollout_ref.rollout.dtype=bfloat16 \
    +actor_rollout_ref.model.override_config.torch_dtype=bfloat16 \
    +ray_init.runtime_env.env_vars.ASYNC_SERVER_HOST="100.64.59.203" \
    +ray_init.runtime_env.env_vars.ASYNC_SERVER_PORT="8133" \
    trainer.validation_data_dir=${PROJECT_DIR}/outputs/valdata_${WANDB_EXP} \
    trainer.log_val_generations=10 $@ > $log_path/grpo_social_${BASE_MODEL##*/}-${BEIJING_TIME}.out 2>&1