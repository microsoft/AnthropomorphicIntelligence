#!/bin/bash
RUN_ID=$(date +"%Y%m%d-%H%M%S")

WORKDIR=$HOME/ds/projects/weicaiyanWorkspace/code/AICompanion/Proact-VL
cd "$WORKDIR"
echo "[Step 2] Work Dir: $WORKDIR"

###############################################
# 3. Start training
###############################################
echo "[Step 3] Begin training..."

N_GPUS=8
GRADIENT_ACC_STEPS=8

RUN_ID=$(date +"%Y%m%d-%H%M%S")
RUN_NAME='proact_lora_base_liveccbase_final'
echo "Time $RUN_ID"

STAGE="strategy3"
ACTIVE_LAYER=-2
echo "Finetune stage: $STAGE, training response head using all clips."

deepspeed --num_gpus=$N_GPUS --master_port 8848 finetune.py \
    --deepspeed ./config/deepspeed_zero2.json \
    --do_train \
    --do_eval \
    --train_dataset_names baldurs_gate_3 csgo cyberpunk_2077 elden_ring lol minecraft starcraft2 streetfighter6 tears_of_the_kingdom yu_gi_oh livecc ego4d \
    --val_dataset_names baldurs_gate_3 csgo cyberpunk_2077 elden_ring lol starcraft2 streetfighter6 tears_of_the_kingdom yu_gi_oh \
    --data_dir_path $HOME/ds/DATA \
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
    --use_lora True \
    --lora_r 32 \
    --lora_alpha 64 \
    --freeze_audio True \
    --freeze_visual True \
    --save_strategy steps \
    --save_steps 250 \
    --save_total_limit 3 \
    --eval_steps 250 \
    --eval_strategy "steps" \
    --report_to "wandb" \
    --run_name $RUN_NAME \
    --gradient_checkpointing True \
    --finetune_strategy ${STAGE} \
    --label_names labels active_labels \
    --active_layer_id ${ACTIVE_LAYER} \
    --output_dir trainer_output/${RUN_NAME}
