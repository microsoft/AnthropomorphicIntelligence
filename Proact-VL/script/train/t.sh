#!/bin/bash
RUN_ID=$(date +"%Y%m%d-%H%M%S")

WORKDIR=$HOME/ds/projects/weicaiyanWorkspace/code/AICompanion/Proact-VL
cd "$WORKDIR"
echo "[Step 2] Work Dir: $WORKDIR"

###############################################
# 3. Start training
###############################################
echo "[Step 3] Begin training..."

N_GPUS=1
GRADIENT_ACC_STEPS=1

RUN_ID=$(date +"%Y%m%d-%H%M%S")
RUN_NAME='proactvl_fulltuning_base_qwen3vl_2b'
echo "Time $RUN_ID"

STAGE="strategy3"
ACTIVE_LAYER=-2
echo "Finetune stage: $STAGE, training response head using all clips."

deepspeed --num_gpus=$N_GPUS --master_port 8848 finetune.py \
    --deepspeed ./config/deepspeed_zero2.json \
    --do_train \
    --do_eval \
    --train_dataset_names yu_gi_oh \
    --val_dataset_names yu_gi_oh \
    --data_dir_path $HOME/DATA/proactvl/proact_sft/DATA \
    --dataloader_num_workers 16 \
    --dataloader_pin_memory True \
    --num_train_epochs 1 \
    --max_steps 5 \
    --learning_rate 1e-5 \
    --max_grad_norm 1.0 \
    --lr_scheduler_type cosine \
    --bf16 \
    --per_device_train_batch_size 1 \
    --per_device_eval_batch_size 1 \
    --gradient_accumulation_steps $GRADIENT_ACC_STEPS \
    --eval_accumulation_steps 4 \
    --logging_steps 5 \
    --model_name_or_path "Qwen/Qwen3-VL-2B-Instruct" \
    --enable_audio_output False \
    --state_threshold 0.5 \
    --loss_active_scale 0.2 \
    --use_lora False \
    --freeze_audio True \
    --freeze_visual True \
    --save_strategy steps \
    --save_steps 5 \
    --save_total_limit 1 \
    --eval_steps 5 \
    --eval_strategy "steps" \
    --report_to "none" \
    --run_name $RUN_NAME \
    --gradient_checkpointing True \
    --finetune_strategy ${STAGE} \
    --label_names labels active_labels \
    --active_layer_id ${ACTIVE_LAYER} \
    --output_dir trainer_output/${RUN_NAME}


