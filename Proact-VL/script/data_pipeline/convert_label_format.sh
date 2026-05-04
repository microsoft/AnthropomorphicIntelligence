SOLO_COMMENTARY_NAMES=("cyberpunk_2077" "starcraft2" "baldurs_gate_3" "black_myth_wukong" "elden_ring" "tears_of_the_kingdom")
SOLO_COMMENTARY_ANNS=("Cyberpunk_2077" "Starcraft2" "Baldurs_Gate_3" "Black_Myth_Wukong" "Elden_Ring" "Tears_of_the_Kingdom")
MULTI_COMMENTARY_NAMES=("yu_gi_oh" "lol" "csgo" "streetfighter6")
MULTI_COMMENTARY_ANNS=("Yu_Gi_Oh" "LOL" "CSGO" "Streetfighter6")
GUIDANCE_NAMES=("minecraft") # "genshin_impact"
GUIDANCE_ANNS=("Minecraft") # "Genshin_Impact"
EGO4D_NAMES=("ego4d_goal_step")
EGO4D_ANNS=("ego4d")
LIVECC_NAMES=("livecc")
LIVECC_ANNS=("LiveCC")
GAME_DIR_NAMES=($SOLO_COMMENTARY_ANNS $MULTI_COMMENTARY_ANNS $GUIDANCE_ANNS)

# ============merge annotations for different datasets ============
if true; then
    # Solo commentators
    python -m proactvl.data.preprocess.merge_anns \
        --dataset_name cyberpunk_2077 \
        --ann_dir DATA/game_commentary/Cyberpunk_2077/raw \
        --video_dir DATA/game_commentary/Cyberpunk_2077/videos \
        --output_file DATA/game_commentary/Cyberpunk_2077/ann/cyberpunk_2077_merged.jsonl \
        --tag 'Solo commentators'

    python -m proactvl.data.preprocess.merge_anns \
        --dataset_name starcraft2 \
        --ann_dir DATA/game_commentary/Starcraft2/raw \
        --video_dir DATA/game_commentary/Starcraft2/videos \
        --output_file DATA/game_commentary/Starcraft2/ann/starcraft2_merged.jsonl \
        --tag 'Solo commentators'

    python -m proactvl.data.preprocess.merge_anns \
        --dataset_name baldurs_gate_3 \
        --ann_dir DATA/game_commentary/Baldurs_Gate_3/raw \
        --video_dir DATA/game_commentary/Baldurs_Gate_3/videos \
        --output_file DATA/game_commentary/Baldurs_Gate_3/ann/baldurs_gate_3_merged.jsonl \
        --tag 'Solo commentators'

    python -m proactvl.data.preprocess.merge_anns \
        --dataset_name black_myth_wukong \
        --ann_dir DATA/game_commentary/Black_Myth_Wukong/raw \
        --video_dir DATA/game_commentary/Black_Myth_Wukong/videos \
        --output_file DATA/game_commentary/Black_Myth_Wukong/ann/black_myth_wukong_merged.jsonl \
        --tag 'Solo commentators'

    python -m proactvl.data.preprocess.merge_anns \
        --dataset_name elden_ring \
        --ann_dir DATA/game_commentary/Elden_Ring/raw \
        --video_dir DATA/game_commentary/Elden_Ring/videos \
        --output_file DATA/game_commentary/Elden_Ring/ann/elden_ring_merged.jsonl \
        --tag 'Solo commentators'

    python -m proactvl.data.preprocess.merge_anns \
        --dataset_name tears_of_the_kingdom \
        --ann_dir DATA/game_commentary/Tears_of_the_Kingdom/raw \
        --video_dir DATA/game_commentary/Tears_of_the_Kingdom/videos \
        --output_file DATA/game_commentary/Tears_of_the_Kingdom/ann/tears_of_the_kingdom_merged.jsonl \
        --tag 'Solo commentators'

    # Multiple commentators
    python -m proactvl.data.preprocess.merge_anns \
        --dataset_name yu_gi_oh \
        --ann_dir DATA/game_commentary/Yu_Gi_Oh/raw \
        --video_dir DATA/game_commentary/Yu_Gi_Oh/videos \
        --output_file DATA/game_commentary/Yu_Gi_Oh/ann/yu_gi_oh_merged.jsonl \
        --tag 'Multiple commentators'

    python -m proactvl.data.preprocess.merge_anns \
        --dataset_name lol \
        --ann_dir DATA/game_commentary/LOL/raw \
        --video_dir DATA/game_commentary/LOL/videos \
        --output_file DATA/game_commentary/LOL/ann/lol_merged.jsonl \
        --tag 'Multiple commentators'

    python -m proactvl.data.preprocess.merge_anns \
        --dataset_name csgo \
        --ann_dir DATA/game_commentary/CSGO/raw \
        --video_dir DATA/game_commentary/CSGO/videos \
        --output_file DATA/game_commentary/CSGO/ann/csgo_merged.jsonl \
        --tag 'Multiple commentators'

    python -m proactvl.data.preprocess.merge_anns \
        --dataset_name streetfighter6 \
        --ann_dir DATA/game_commentary/Streetfighter6/raw \
        --video_dir DATA/game_commentary/Streetfighter6/videos \
        --output_file DATA/game_commentary/Streetfighter6/ann/streetfighter6_merged.jsonl \
        --tag 'Multiple commentators'

    # # ==================TODO================
    # # Guidance
    # ## minecraft
    python -m proactvl.data.preprocess.merge_anns \
        --dataset_name minecraft \
        --ann_dir DATA/game_commentary/Minecraft/raw \
        --video_dir DATA/game_commentary/Minecraft/videos \
        --output_file DATA/game_commentary/Minecraft/ann/minecraft_merged.jsonl \
        --tag 'Guidance'

    # General
    ## ego4d
    python -m proactvl.data.preprocess.merge_anns \
        --dataset_name ego4d_goal_step \
        --ann_dir DATA/ego4d/v2/raw \
        --video_dir DATA/ego4d/v2/full_scale \
        --output_file DATA/ego4d/v2/ann/ego4d_merged.jsonl \
        --tag 'ego4d'


# ===========convert *_merge_*.jsonl into standard format =============
if true; then
    python -m proactvl.data.preprocess.preprocess --ann_dir DATA/game_commentary/Baldurs_Gate_3/ann
    python -m proactvl.data.preprocess.preprocess --ann_dir DATA/game_commentary/CSGO/ann
    python -m proactvl.data.preprocess.preprocess --ann_dir DATA/game_commentary/Cyberpunk_2077/ann
    python -m proactvl.data.preprocess.preprocess --ann_dir DATA/game_commentary/Elden_Ring/ann
    python -m proactvl.data.preprocess.preprocess --ann_dir DATA/game_commentary/LOL/ann
    python -m proactvl.data.preprocess.preprocess --ann_dir DATA/game_commentary/Starcraft2/ann
    python -m proactvl.data.preprocess.preprocess --ann_dir DATA/game_commentary/Streetfighter6/ann
    python -m proactvl.data.preprocess.preprocess --ann_dir DATA/game_commentary/Tears_of_the_Kingdom/ann
    python -m proactvl.data.preprocess.preprocess --ann_dir DATA/game_commentary/Yu_Gi_Oh/ann
    python -m proactvl.data.preprocess.preprocess --ann_dir DATA/game_commentary/Minecraft/ann
    
    ## ego4d
    python -m proactvl.data.preprocess.preprocess --ann_dir DATA/ego4d/v2/ann
    python -m proactvl.data.preprocess.preprocess --ann_dir DATA/game_commentary/Black_Myth_Wukong/ann
# ===========convert *_standard_*.jsonl into training format =============
if true; then
    python -m proactvl.data.preprocess.prepare_for_training --ann_dir DATA/game_commentary/Baldurs_Gate_3/ann \
        --clip_duration 36 --clip_overlap 18 --min_duration 18 --history_duration 60 --min_active_rate 0.0 --max_active_rate 0.0
    python -m proactvl.data.preprocess.prepare_for_training --ann_dir DATA/game_commentary/Baldurs_Gate_3/ann \
        --clip_duration 36 --clip_overlap 18 --min_duration 18 --history_duration 60 --min_active_rate 0.0 --max_active_rate 0.3
    python -m proactvl.data.preprocess.prepare_for_training --ann_dir DATA/game_commentary/Baldurs_Gate_3/ann \
        --clip_duration 36 --clip_overlap 18 --min_duration 18 --history_duration 60 --min_active_rate 0.3 --max_active_rate 0.7
    python -m proactvl.data.preprocess.prepare_for_training --ann_dir DATA/game_commentary/Baldurs_Gate_3/ann \
        --clip_duration 36 --clip_overlap 18 --min_duration 18 --history_duration 60 --min_active_rate 0.7 --max_active_rate 1.0

    python -m proactvl.data.preprocess.prepare_for_training --ann_dir DATA/game_commentary/Black_Myth_Wukong/ann \
        --clip_duration 36 --clip_overlap 18 --min_duration 18 --history_duration 60 --min_active_rate 0.0 --max_active_rate 0.0
    python -m proactvl.data.preprocess.prepare_for_training --ann_dir DATA/game_commentary/Black_Myth_Wukong/ann \
        --clip_duration 36 --clip_overlap 18 --min_duration 18 --history_duration 60 --min_active_rate 0.0 --max_active_rate 0.3
    python -m proactvl.data.preprocess.prepare_for_training --ann_dir DATA/game_commentary/Black_Myth_Wukong/ann \
        --clip_duration 36 --clip_overlap 18 --min_duration 18 --history_duration 60 --min_active_rate 0.3 --max_active_rate 0.7
    python -m proactvl.data.preprocess.prepare_for_training --ann_dir DATA/game_commentary/Black_Myth_Wukong/ann \
        --clip_duration 36 --clip_overlap 18 --min_duration 18 --history_duration 60 --min_active_rate 0.7 --max_active_rate 1.0

    python -m proactvl.data.preprocess.prepare_for_training --ann_dir DATA/game_commentary/CSGO/ann \
        --clip_duration 36 --clip_overlap 18 --min_duration 18 --history_duration 60 --min_active_rate 0.0 --max_active_rate 0.0
    python -m proactvl.data.preprocess.prepare_for_training --ann_dir DATA/game_commentary/CSGO/ann \
        --clip_duration 36 --clip_overlap 18 --min_duration 18 --history_duration 60 --min_active_rate 0.0 --max_active_rate 0.3
    python -m proactvl.data.preprocess.prepare_for_training --ann_dir DATA/game_commentary/CSGO/ann \
        --clip_duration 36 --clip_overlap 18 --min_duration 18 --history_duration 60 --min_active_rate 0.3 --max_active_rate 0.7
    python -m proactvl.data.preprocess.prepare_for_training --ann_dir DATA/game_commentary/CSGO/ann \
        --clip_duration 36 --clip_overlap 18 --min_duration 18 --history_duration 60 --min_active_rate 0.7 --max_active_rate 1.0

    python -m proactvl.data.preprocess.prepare_for_training --ann_dir DATA/game_commentary/Cyberpunk_2077/ann \
        --clip_duration 36 --clip_overlap 18 --min_duration 18 --history_duration 60 --min_active_rate 0.0 --max_active_rate 0.0
    python -m proactvl.data.preprocess.prepare_for_training --ann_dir DATA/game_commentary/Cyberpunk_2077/ann \
        --clip_duration 36 --clip_overlap 18 --min_duration 18 --history_duration 60 --min_active_rate 0.0 --max_active_rate 0.3
    python -m proactvl.data.preprocess.prepare_for_training --ann_dir DATA/game_commentary/Cyberpunk_2077/ann \
        --clip_duration 36 --clip_overlap 18 --min_duration 18 --history_duration 60 --min_active_rate 0.3 --max_active_rate 0.7
    python -m proactvl.data.preprocess.prepare_for_training --ann_dir DATA/game_commentary/Cyberpunk_2077/ann \
        --clip_duration 36 --clip_overlap 18 --min_duration 18 --history_duration 60 --min_active_rate 0.7 --max_active_rate 1.0

    python -m proactvl.data.preprocess.prepare_for_training --ann_dir DATA/game_commentary/Elden_Ring/ann \
        --clip_duration 36 --clip_overlap 18 --min_duration 18 --history_duration 60 --min_active_rate 0.0 --max_active_rate 0.0
    python -m proactvl.data.preprocess.prepare_for_training --ann_dir DATA/game_commentary/Elden_Ring/ann \
        --clip_duration 36 --clip_overlap 18 --min_duration 18 --history_duration 60 --min_active_rate 0.0 --max_active_rate 0.3
    python -m proactvl.data.preprocess.prepare_for_training --ann_dir DATA/game_commentary/Elden_Ring/ann \
        --clip_duration 36 --clip_overlap 18 --min_duration 18 --history_duration 60 --min_active_rate 0.3 --max_active_rate 0.7
    python -m proactvl.data.preprocess.prepare_for_training --ann_dir DATA/game_commentary/Elden_Ring/ann \
        --clip_duration 36 --clip_overlap 18 --min_duration 18 --history_duration 60 --min_active_rate 0.7 --max_active_rate 1.0

    python -m proactvl.data.preprocess.prepare_for_training --ann_dir DATA/game_commentary/LOL/ann \
        --clip_duration 36 --clip_overlap 18 --min_duration 18 --history_duration 60 --min_active_rate 0.0 --max_active_rate 0.0
    python -m proactvl.data.preprocess.prepare_for_training --ann_dir DATA/game_commentary/LOL/ann \
        --clip_duration 36 --clip_overlap 18 --min_duration 18 --history_duration 60 --min_active_rate 0.0 --max_active_rate 0.3
    python -m proactvl.data.preprocess.prepare_for_training --ann_dir DATA/game_commentary/LOL/ann \
        --clip_duration 36 --clip_overlap 18 --min_duration 18 --history_duration 60 --min_active_rate 0.3 --max_active_rate 0.7
    python -m proactvl.data.preprocess.prepare_for_training --ann_dir DATA/game_commentary/LOL/ann \
        --clip_duration 36 --clip_overlap 18 --min_duration 18 --history_duration 60 --min_active_rate 0.7 --max_active_rate 1.0

    python -m proactvl.data.preprocess.prepare_for_training --ann_dir DATA/game_commentary/Starcraft2/ann \
        --clip_duration 36 --clip_overlap 18 --min_duration 18 --history_duration 60 --min_active_rate 0.0 --max_active_rate 0.0
    python -m proactvl.data.preprocess.prepare_for_training --ann_dir DATA/game_commentary/Starcraft2/ann \
        --clip_duration 36 --clip_overlap 18 --min_duration 18 --history_duration 60 --min_active_rate 0.0 --max_active_rate 0.3
    python -m proactvl.data.preprocess.prepare_for_training --ann_dir DATA/game_commentary/Starcraft2/ann \
        --clip_duration 36 --clip_overlap 18 --min_duration 18 --history_duration 60 --min_active_rate 0.3 --max_active_rate 0.7
    python -m proactvl.data.preprocess.prepare_for_training --ann_dir DATA/game_commentary/Starcraft2/ann \
        --clip_duration 36 --clip_overlap 18 --min_duration 18 --history_duration 60 --min_active_rate 0.7 --max_active_rate 1.0

    python -m proactvl.data.preprocess.prepare_for_training --ann_dir DATA/game_commentary/Streetfighter6/ann \
        --clip_duration 36 --clip_overlap 18 --min_duration 18 --history_duration 60 --min_active_rate 0.0 --max_active_rate 0.0
    python -m proactvl.data.preprocess.prepare_for_training --ann_dir DATA/game_commentary/Streetfighter6/ann \
        --clip_duration 36 --clip_overlap 18 --min_duration 18 --history_duration 60 --min_active_rate 0.0 --max_active_rate 0.3
    python -m proactvl.data.preprocess.prepare_for_training --ann_dir DATA/game_commentary/Streetfighter6/ann \
        --clip_duration 36 --clip_overlap 18 --min_duration 18 --history_duration 60 --min_active_rate 0.3 --max_active_rate 0.7
    python -m proactvl.data.preprocess.prepare_for_training --ann_dir DATA/game_commentary/Streetfighter6/ann \
        --clip_duration 36 --clip_overlap 18 --min_duration 18 --history_duration 60 --min_active_rate 0.7 --max_active_rate 1.0

    python -m proactvl.data.preprocess.prepare_for_training --ann_dir DATA/game_commentary/Tears_of_the_Kingdom/ann \
        --clip_duration 36 --clip_overlap 18 --min_duration 18 --history_duration 60 --min_active_rate 0.0 --max_active_rate 0.0
    python -m proactvl.data.preprocess.prepare_for_training --ann_dir DATA/game_commentary/Tears_of_the_Kingdom/ann \
        --clip_duration 36 --clip_overlap 18 --min_duration 18 --history_duration 60 --min_active_rate 0.0 --max_active_rate 0.3
    python -m proactvl.data.preprocess.prepare_for_training --ann_dir DATA/game_commentary/Tears_of_the_Kingdom/ann \
        --clip_duration 36 --clip_overlap 18 --min_duration 18 --history_duration 60 --min_active_rate 0.3 --max_active_rate 0.7
    python -m proactvl.data.preprocess.prepare_for_training --ann_dir DATA/game_commentary/Tears_of_the_Kingdom/ann \
        --clip_duration 36 --clip_overlap 18 --min_duration 18 --history_duration 60 --min_active_rate 0.7 --max_active_rate 1.0

    python -m proactvl.data.preprocess.prepare_for_training --ann_dir DATA/game_commentary/Yu_Gi_Oh/ann \
        --clip_duration 36 --clip_overlap 18 --min_duration 18 --history_duration 60 --min_active_rate 0.0 --max_active_rate 0.0
    python -m proactvl.data.preprocess.prepare_for_training --ann_dir DATA/game_commentary/Yu_Gi_Oh/ann \
        --clip_duration 36 --clip_overlap 18 --min_duration 18 --history_duration 60 --min_active_rate 0.0 --max_active_rate 0.3
    python -m proactvl.data.preprocess.prepare_for_training --ann_dir DATA/game_commentary/Yu_Gi_Oh/ann \
        --clip_duration 36 --clip_overlap 18 --min_duration 18 --history_duration 60 --min_active_rate 0.3 --max_active_rate 0.7
    python -m proactvl.data.preprocess.prepare_for_training --ann_dir DATA/game_commentary/Yu_Gi_Oh/ann \
        --clip_duration 36 --clip_overlap 18 --min_duration 18 --history_duration 60 --min_active_rate 0.7 --max_active_rate 1.0

    python -m proactvl.data.preprocess.prepare_for_training --ann_dir DATA/game_commentary/Minecraft/ann \
        --clip_duration 36 --clip_overlap 18 --min_duration 18 --history_duration 300 --min_active_rate 0.0 --max_active_rate 0.0
    python -m proactvl.data.preprocess.prepare_for_training --ann_dir DATA/game_commentary/Minecraft/ann \
        --clip_duration 36 --clip_overlap 18 --min_duration 18 --history_duration 300 --min_active_rate 0.0 --max_active_rate 0.3
    python -m proactvl.data.preprocess.prepare_for_training --ann_dir DATA/game_commentary/Minecraft/ann \
        --clip_duration 36 --clip_overlap 18 --min_duration 18 --history_duration 300 --min_active_rate 0.3 --max_active_rate 0.7
    python -m proactvl.data.preprocess.prepare_for_training --ann_dir DATA/game_commentary/Minecraft/ann \
        --clip_duration 36 --clip_overlap 18 --min_duration 18 --history_duration 300 --min_active_rate 0.7 --max_active_rate 1.0

    python -m proactvl.data.preprocess.prepare_for_training --ann_dir DATA/game_commentary/Minecraft/ann \
        --clip_duration 60 --clip_overlap 30 --min_duration 30 --history_duration 300 --min_active_rate 0.0 --max_active_rate 0.0
    python -m proactvl.data.preprocess.prepare_for_training --ann_dir DATA/game_commentary/Minecraft/ann \
        --clip_duration 60 --clip_overlap 30 --min_duration 30 --history_duration 300 --min_active_rate 0.0 --max_active_rate 0.3
    python -m proactvl.data.preprocess.prepare_for_training --ann_dir DATA/game_commentary/Minecraft/ann \
        --clip_duration 60 --clip_overlap 30 --min_duration 30 --history_duration 300 --min_active_rate 0.3 --max_active_rate 0.7
    python -m proactvl.data.preprocess.prepare_for_training --ann_dir DATA/game_commentary/Minecraft/ann \
        --clip_duration 60 --clip_overlap 30 --min_duration 30 --history_duration 300 --min_active_rate 0.7 --max_active_rate 1.0

    python -m proactvl.data.preprocess.prepare_for_training --ann_dir DATA/ego4d/v2/ann \
        --clip_duration 60 --clip_overlap 30 --min_duration 30 --history_duration 300 --min_active_rate 0.0 --max_active_rate 0.0
    python -m proactvl.data.preprocess.prepare_for_training --ann_dir DATA/ego4d/v2/ann \
        --clip_duration 60 --clip_overlap 30 --min_duration 30 --history_duration 300 --min_active_rate 0.0 --max_active_rate 0.3
    python -m proactvl.data.preprocess.prepare_for_training --ann_dir DATA/ego4d/v2/ann \
        --clip_duration 60 --clip_overlap 30 --min_duration 30 --history_duration 300 --min_active_rate 0.3 --max_active_rate 0.7
    python -m proactvl.data.preprocess.prepare_for_training --ann_dir DATA/ego4d/v2/ann \
        --clip_duration 60 --clip_overlap 30 --min_duration 30 --history_duration 300 --min_active_rate 0.7 --max_active_rate 1.0

    # for val
    python -m proactvl.data.preprocess.prepare_for_training --ann_dir DATA/ego4d/v2/ann \
        --clip_duration 300 --clip_overlap 0 --min_duration 0 --history_duration 0 --min_active_rate 0.0 --max_active_rate 0.0
    python -m proactvl.data.preprocess.prepare_for_training --ann_dir DATA/ego4d/v2/ann \
        --clip_duration 300 --clip_overlap 0 --min_duration 0 --history_duration 0 --min_active_rate 0.0 --max_active_rate 1.0


# summary

python -m proactvl.data.preprocess.summary --ann_dir DATA/game_commentary/Baldurs_Gate_3/ann
python -m proactvl.data.preprocess.summary --ann_dir DATA/game_commentary/Black_Myth_Wukong/ann
python -m proactvl.data.preprocess.summary --ann_dir DATA/game_commentary/CSGO/ann
python -m proactvl.data.preprocess.summary --ann_dir DATA/game_commentary/Cyberpunk_2077/ann
python -m proactvl.data.preprocess.summary --ann_dir DATA/game_commentary/Elden_Ring/ann
python -m proactvl.data.preprocess.summary --ann_dir DATA/game_commentary/LOL/ann
python -m proactvl.data.preprocess.summary --ann_dir DATA/game_commentary/Starcraft2/ann
python -m proactvl.data.preprocess.summary --ann_dir DATA/game_commentary/Streetfighter6/ann
python -m proactvl.data.preprocess.summary --ann_dir DATA/game_commentary/Tears_of_the_Kingdom/ann
python -m proactvl.data.preprocess.summary --ann_dir DATA/game_commentary/Yu_Gi_Oh/ann
python -m proactvl.data.preprocess.summary --ann_dir DATA/game_commentary/Minecraft/ann
python -m proactvl.data.preprocess.summary --ann_dir DATA/ego4d/v2/ann
# randomly select training samples
# 279	8993	3831
python -m proactvl.data.preprocess.post_preprocess --input_files \
    DATA/game_commentary/Baldurs_Gate_3/ann/baldurs_gate_3_split_clips_36s_overlap18s_0.0-0.0_train.jsonl \
    DATA/game_commentary/Baldurs_Gate_3/ann/baldurs_gate_3_split_clips_36s_overlap18s_0.0-0.3_train.jsonl \
    DATA/game_commentary/Baldurs_Gate_3/ann/baldurs_gate_3_split_clips_36s_overlap18s_0.3-0.7_train.jsonl \
    DATA/game_commentary/Baldurs_Gate_3/ann/baldurs_gate_3_split_clips_36s_overlap18s_0.7-1.0_train.jsonl \
    --output_file DATA/ann/baldurs_gate_3_final_train.jsonl \
    --select_nums 0 '-1' 7000 3000
# 1027	1575	210
python -m proactvl.data.preprocess.post_preprocess --input_files \
    DATA/game_commentary/Black_Myth_Wukong/ann/black_myth_wukong_split_clips_36s_overlap18s_0.0-0.0_train.jsonl \
    DATA/game_commentary/Black_Myth_Wukong/ann/black_myth_wukong_split_clips_36s_overlap18s_0.0-0.3_train.jsonl \
    DATA/game_commentary/Black_Myth_Wukong/ann/black_myth_wukong_split_clips_36s_overlap18s_0.3-0.7_train.jsonl \
    DATA/game_commentary/Black_Myth_Wukong/ann/black_myth_wukong_split_clips_36s_overlap18s_0.7-1.0_train.jsonl \
    --output_file DATA/ann/black_myth_wukong_final_train.jsonl \
    --select_nums 0 '-1' '-1' '-1'
# 2015	3942	4390
python -m proactvl.data.preprocess.post_preprocess --input_files \
    DATA/game_commentary/CSGO/ann/csgo_split_clips_36s_overlap18s_0.0-0.0_train.jsonl \
    DATA/game_commentary/CSGO/ann/csgo_split_clips_36s_overlap18s_0.0-0.3_train.jsonl \
    DATA/game_commentary/CSGO/ann/csgo_split_clips_36s_overlap18s_0.3-0.7_train.jsonl \
    DATA/game_commentary/CSGO/ann/csgo_split_clips_36s_overlap18s_0.7-1.0_train.jsonl \
    --output_file DATA/ann/csgo_final_train.jsonl \
    --select_nums 0 '-1' '-1' '-1'
# 2792	3604	1601
python -m proactvl.data.preprocess.post_preprocess --input_files \
    DATA/game_commentary/Cyberpunk_2077/ann/cyberpunk_2077_split_clips_36s_overlap18s_0.0-0.0_train.jsonl \
    DATA/game_commentary/Cyberpunk_2077/ann/cyberpunk_2077_split_clips_36s_overlap18s_0.0-0.3_train.jsonl \
    DATA/game_commentary/Cyberpunk_2077/ann/cyberpunk_2077_split_clips_36s_overlap18s_0.3-0.7_train.jsonl \
    DATA/game_commentary/Cyberpunk_2077/ann/cyberpunk_2077_split_clips_36s_overlap18s_0.7-1.0_train.jsonl \
    --output_file DATA/ann/cyberpunk_2077_final_train.jsonl \
    --select_nums 0 '-1' '-1' '-1'
# 934	4017	2448
python -m proactvl.data.preprocess.post_preprocess --input_files \
    DATA/game_commentary/Elden_Ring/ann/elden_ring_split_clips_36s_overlap18s_0.0-0.0_train.jsonl \
    DATA/game_commentary/Elden_Ring/ann/elden_ring_split_clips_36s_overlap18s_0.0-0.3_train.jsonl \
    DATA/game_commentary/Elden_Ring/ann/elden_ring_split_clips_36s_overlap18s_0.3-0.7_train.jsonl \
    DATA/game_commentary/Elden_Ring/ann/elden_ring_split_clips_36s_overlap18s_0.7-1.0_train.jsonl \
    --output_file DATA/ann/elden_ring_final_train.jsonl \
    --select_nums 0 '-1' '-1' '-1'
# 1151	2437	1918
python -m proactvl.data.preprocess.post_preprocess --input_files \
    DATA/game_commentary/LOL/ann/lol_split_clips_36s_overlap18s_0.0-0.0_train.jsonl \
    DATA/game_commentary/LOL/ann/lol_split_clips_36s_overlap18s_0.0-0.3_train.jsonl \
    DATA/game_commentary/LOL/ann/lol_split_clips_36s_overlap18s_0.3-0.7_train.jsonl \
    DATA/game_commentary/LOL/ann/lol_split_clips_36s_overlap18s_0.7-1.0_train.jsonl \
    --output_file DATA/ann/lol_final_train.jsonl \
    --select_nums 0 '-1' '-1' '-1'
# 1393	3934	6500
python -m proactvl.data.preprocess.post_preprocess --input_files \
    DATA/game_commentary/Starcraft2/ann/starcraft2_split_clips_36s_overlap18s_0.0-0.0_train.jsonl \
    DATA/game_commentary/Starcraft2/ann/starcraft2_split_clips_36s_overlap18s_0.0-0.3_train.jsonl \
    DATA/game_commentary/Starcraft2/ann/starcraft2_split_clips_36s_overlap18s_0.3-0.7_train.jsonl \
    DATA/game_commentary/Starcraft2/ann/starcraft2_split_clips_36s_overlap18s_0.7-1.0_train.jsonl \
    --output_file DATA/ann/starcraft2_final_train.jsonl \
    --select_nums 0 '-1' '-1' '-1'
# 2401	6021	4529
python -m proactvl.data.preprocess.post_preprocess --input_files \
    DATA/game_commentary/Streetfighter6/ann/streetfighter6_split_clips_36s_overlap18s_0.0-0.0_train.jsonl \
    DATA/game_commentary/Streetfighter6/ann/streetfighter6_split_clips_36s_overlap18s_0.0-0.3_train.jsonl \
    DATA/game_commentary/Streetfighter6/ann/streetfighter6_split_clips_36s_overlap18s_0.3-0.7_train.jsonl \
    DATA/game_commentary/Streetfighter6/ann/streetfighter6_split_clips_36s_overlap18s_0.7-1.0_train.jsonl \
    --output_file DATA/ann/streetfighter6_final_train.jsonl \
    --select_nums 0 2000 5000 3000
# 1407	7068	2164
python -m proactvl.data.preprocess.post_preprocess --input_files \
    DATA/game_commentary/Tears_of_the_Kingdom/ann/tears_of_the_kingdom_split_clips_36s_overlap18s_0.0-0.0_train.jsonl \
    DATA/game_commentary/Tears_of_the_Kingdom/ann/tears_of_the_kingdom_split_clips_36s_overlap18s_0.0-0.3_train.jsonl \
    DATA/game_commentary/Tears_of_the_Kingdom/ann/tears_of_the_kingdom_split_clips_36s_overlap18s_0.3-0.7_train.jsonl \
    DATA/game_commentary/Tears_of_the_Kingdom/ann/tears_of_the_kingdom_split_clips_36s_overlap18s_0.7-1.0_train.jsonl \
    --output_file DATA/ann/tears_of_the_kingdom_final_train.jsonl \
    --select_nums 0 1200 6877 2000
# 771	1621	791
python -m proactvl.data.preprocess.post_preprocess --input_files \
    DATA/game_commentary/Yu_Gi_Oh/ann/yu_gi_oh_split_clips_36s_overlap18s_0.0-0.0_train.jsonl \
    DATA/game_commentary/Yu_Gi_Oh/ann/yu_gi_oh_split_clips_36s_overlap18s_0.0-0.3_train.jsonl \
    DATA/game_commentary/Yu_Gi_Oh/ann/yu_gi_oh_split_clips_36s_overlap18s_0.3-0.7_train.jsonl \
    DATA/game_commentary/Yu_Gi_Oh/ann/yu_gi_oh_split_clips_36s_overlap18s_0.7-1.0_train.jsonl \
    --output_file DATA/ann/yu_gi_oh_final_train.jsonl \
    --select_nums 0 '-1' '-1' '-1'
# 1864	1996	101
python -m proactvl.data.preprocess.post_preprocess --input_files \
    DATA/game_commentary/Minecraft/ann/minecraft_split_clips_36s_overlap18s_0.0-0.0_train.jsonl \
    DATA/game_commentary/Minecraft/ann/minecraft_split_clips_36s_overlap18s_0.0-0.3_train.jsonl \
    DATA/game_commentary/Minecraft/ann/minecraft_split_clips_36s_overlap18s_0.3-0.7_train.jsonl \
    DATA/game_commentary/Minecraft/ann/minecraft_split_clips_36s_overlap18s_0.7-1.0_train.jsonl \
    DATA/game_commentary/Minecraft/ann/minecraft_split_clips_60s_overlap30s_0.0-0.0_train.jsonl \
    DATA/game_commentary/Minecraft/ann/minecraft_split_clips_60s_overlap30s_0.0-0.3_train.jsonl \
    DATA/game_commentary/Minecraft/ann/minecraft_split_clips_60s_overlap30s_0.3-0.7_train.jsonl \
    DATA/game_commentary/Minecraft/ann/minecraft_split_clips_60s_overlap30s_0.7-1.0_train.jsonl \
    --output_file DATA/ann/minecraft_final_train.jsonl \
    --select_nums 0 '-1' '-1' '-1' 0 '-1' '-1' '-1'

python -m proactvl.data.preprocess.post_preprocess --input_files \
    DATA/ego4d/v2/ann/ego4d_split_clips_60s_overlap30s_0.0-0.0_train.jsonl \
    DATA/ego4d/v2/ann/ego4d_split_clips_60s_overlap30s_0.0-0.3_train.jsonl \
    DATA/ego4d/v2/ann/ego4d_split_clips_60s_overlap30s_0.3-0.7_train.jsonl \
    DATA/ego4d/v2/ann/ego4d_split_clips_60s_overlap30s_0.7-1.0_train.jsonl \
    --output_file DATA/ann/ego4d_final_train.jsonl \
    --select_nums 0 '-1' '-1' '-1'

# ============================special handle ============================
# Baldur's Gate 3 and Black Myth Wukong have insufficient val data; fill with test data
python -m proactvl.data.preprocess.merge_anns \
    --dataset_name baldurs_gate_3 \
    --ann_dir DATA/game_commentary/Baldurs_Gate_3/raw \
    --video_dir DATA/game_commentary/Baldurs_Gate_3/videos \
    --output_file DATA/game_commentary/Baldurs_Gate_3/ann/baldurs_gate_3_merged.jsonl \
    --tag 'Solo commentators' \
    --dataset_type_list test

python -m proactvl.data.preprocess.preprocess --ann_dir DATA/game_commentary/Baldurs_Gate_3/ann --dataset_type_list test

python -m proactvl.data.preprocess.prepare_for_training --ann_dir DATA/game_commentary/Baldurs_Gate_3/ann \
    --clip_duration 36 --clip_overlap 18 --min_duration 18 --history_duration 60 --min_active_rate 0.0 --max_active_rate 0.0 --dataset_type_list test
python -m proactvl.data.preprocess.prepare_for_training --ann_dir DATA/game_commentary/Baldurs_Gate_3/ann \
    --clip_duration 36 --clip_overlap 18 --min_duration 18 --history_duration 60 --min_active_rate 0.0 --max_active_rate 0.3 --dataset_type_list test
python -m proactvl.data.preprocess.prepare_for_training --ann_dir DATA/game_commentary/Baldurs_Gate_3/ann \
    --clip_duration 36 --clip_overlap 18 --min_duration 18 --history_duration 60 --min_active_rate 0.3 --max_active_rate 0.7 --dataset_type_list test
python -m proactvl.data.preprocess.prepare_for_training --ann_dir DATA/game_commentary/Baldurs_Gate_3/ann \
    --clip_duration 36 --clip_overlap 18 --min_duration 18 --history_duration 60 --min_active_rate 0.7 --max_active_rate 1.0 --dataset_type_list test

python -m proactvl.data.preprocess.merge_anns \
    --dataset_name black_myth_wukong \
    --ann_dir DATA/game_commentary/Black_Myth_Wukong/raw \
    --video_dir DATA/game_commentary/Black_Myth_Wukong/videos \
    --output_file DATA/game_commentary/Black_Myth_Wukong/ann/black_myth_wukong_merged.jsonl \
    --tag 'Solo commentators' \
    --dataset_type_list test

python -m proactvl.data.preprocess.preprocess --ann_dir DATA/game_commentary/Black_Myth_Wukong/ann --dataset_type_list test

python -m proactvl.data.preprocess.prepare_for_training --ann_dir DATA/game_commentary/Black_Myth_Wukong/ann \
    --clip_duration 36 --clip_overlap 18 --min_duration 18 --history_duration 60 --min_active_rate 0.0 --max_active_rate 0.0 --dataset_type_list test
python -m proactvl.data.preprocess.prepare_for_training --ann_dir DATA/game_commentary/Black_Myth_Wukong/ann \
    --clip_duration 36 --clip_overlap 18 --min_duration 18 --history_duration 60 --min_active_rate 0.0 --max_active_rate 0.3 --dataset_type_list test
python -m proactvl.data.preprocess.prepare_for_training --ann_dir DATA/game_commentary/Black_Myth_Wukong/ann \
    --clip_duration 36 --clip_overlap 18 --min_duration 18 --history_duration 60 --min_active_rate 0.3 --max_active_rate 0.7 --dataset_type_list test
python -m proactvl.data.preprocess.prepare_for_training --ann_dir DATA/game_commentary/Black_Myth_Wukong/ann \
    --clip_duration 36 --clip_overlap 18 --min_duration 18 --history_duration 60 --min_active_rate 0.7 --max_active_rate 1.0 --dataset_type_list test
    
# ================================ randomly select val samples ====================================
python -m proactvl.data.preprocess.post_preprocess --input_files \
    DATA/game_commentary/Baldurs_Gate_3/ann/baldurs_gate_3_split_clips_36s_overlap18s_0.0-0.3_test.jsonl \
    DATA/game_commentary/Baldurs_Gate_3/ann/baldurs_gate_3_split_clips_36s_overlap18s_0.0-0.3_val.jsonl \
    DATA/game_commentary/Baldurs_Gate_3/ann/baldurs_gate_3_split_clips_36s_overlap18s_0.3-0.7_val.jsonl \
    DATA/game_commentary/Baldurs_Gate_3/ann/baldurs_gate_3_split_clips_36s_overlap18s_0.7-1.0_val.jsonl \
    --output_file DATA/ann/baldurs_gate_3_final_val.jsonl \
    --select_nums 30 30 120 60
# 1027	1575	210
python -m proactvl.data.preprocess.post_preprocess --input_files \
    DATA/game_commentary/Black_Myth_Wukong/ann/black_myth_wukong_split_clips_36s_overlap18s_0.0-0.3_test.jsonl \
    DATA/game_commentary/Black_Myth_Wukong/ann/black_myth_wukong_split_clips_36s_overlap18s_0.0-0.3_val.jsonl \
    DATA/game_commentary/Black_Myth_Wukong/ann/black_myth_wukong_split_clips_36s_overlap18s_0.3-0.7_val.jsonl \
    DATA/game_commentary/Black_Myth_Wukong/ann/black_myth_wukong_split_clips_36s_overlap18s_0.7-1.0_val.jsonl \
    DATA/game_commentary/Black_Myth_Wukong/ann/black_myth_wukong_split_clips_36s_overlap18s_0.7-1.0_test.jsonl \
    --output_file DATA/ann/black_myth_wukong_final_val.jsonl \
    --select_nums 30 30 120 30 30
# 2015	3942	4390
python -m proactvl.data.preprocess.post_preprocess --input_files \
    DATA/game_commentary/CSGO/ann/csgo_split_clips_36s_overlap18s_0.0-0.3_val.jsonl \
    DATA/game_commentary/CSGO/ann/csgo_split_clips_36s_overlap18s_0.3-0.7_val.jsonl \
    DATA/game_commentary/CSGO/ann/csgo_split_clips_36s_overlap18s_0.7-1.0_val.jsonl \
    --output_file DATA/ann/csgo_final_val.jsonl \
    --select_nums 60 120 60
# 2792	3604	1601
python -m proactvl.data.preprocess.post_preprocess --input_files \
    DATA/game_commentary/Cyberpunk_2077/ann/cyberpunk_2077_split_clips_36s_overlap18s_0.0-0.3_val.jsonl \
    DATA/game_commentary/Cyberpunk_2077/ann/cyberpunk_2077_split_clips_36s_overlap18s_0.3-0.7_val.jsonl \
    DATA/game_commentary/Cyberpunk_2077/ann/cyberpunk_2077_split_clips_36s_overlap18s_0.7-1.0_val.jsonl \
    --output_file DATA/ann/cyberpunk_2077_final_val.jsonl \
    --select_nums 60 120 60
# 934	4017	2448
python -m proactvl.data.preprocess.post_preprocess --input_files \
    DATA/game_commentary/Elden_Ring/ann/elden_ring_split_clips_36s_overlap18s_0.0-0.3_val.jsonl \
    DATA/game_commentary/Elden_Ring/ann/elden_ring_split_clips_36s_overlap18s_0.3-0.7_val.jsonl \
    DATA/game_commentary/Elden_Ring/ann/elden_ring_split_clips_36s_overlap18s_0.7-1.0_val.jsonl \
    --output_file DATA/ann/elden_ring_final_val.jsonl \
    --select_nums 60 120 60
# 1151	2437	1918
python -m proactvl.data.preprocess.post_preprocess --input_files \
    DATA/game_commentary/LOL/ann/lol_split_clips_36s_overlap18s_0.0-0.3_val.jsonl \
    DATA/game_commentary/LOL/ann/lol_split_clips_36s_overlap18s_0.3-0.7_val.jsonl \
    DATA/game_commentary/LOL/ann/lol_split_clips_36s_overlap18s_0.7-1.0_val.jsonl \
    --output_file DATA/ann/lol_final_val.jsonl \
    --select_nums 60 120 60
# 1393	3934	6500
python -m proactvl.data.preprocess.post_preprocess --input_files \
    DATA/game_commentary/Starcraft2/ann/starcraft2_split_clips_36s_overlap18s_0.0-0.3_val.jsonl \
    DATA/game_commentary/Starcraft2/ann/starcraft2_split_clips_36s_overlap18s_0.3-0.7_val.jsonl \
    DATA/game_commentary/Starcraft2/ann/starcraft2_split_clips_36s_overlap18s_0.7-1.0_val.jsonl \
    --output_file DATA/ann/starcraft2_final_val.jsonl \
    --select_nums 60 120 60
# 2401	6021	4529
python -m proactvl.data.preprocess.post_preprocess --input_files \
    DATA/game_commentary/Streetfighter6/ann/streetfighter6_split_clips_36s_overlap18s_0.0-0.3_val.jsonl \
    DATA/game_commentary/Streetfighter6/ann/streetfighter6_split_clips_36s_overlap18s_0.3-0.7_val.jsonl \
    DATA/game_commentary/Streetfighter6/ann/streetfighter6_split_clips_36s_overlap18s_0.7-1.0_val.jsonl \
    --output_file DATA/ann/streetfighter6_final_val.jsonl \
    --select_nums 60 120 60
# 1407	7068	2164
python -m proactvl.data.preprocess.post_preprocess --input_files \
    DATA/game_commentary/Tears_of_the_Kingdom/ann/tears_of_the_kingdom_split_clips_36s_overlap18s_0.0-0.3_val.jsonl \
    DATA/game_commentary/Tears_of_the_Kingdom/ann/tears_of_the_kingdom_split_clips_36s_overlap18s_0.3-0.7_val.jsonl \
    DATA/game_commentary/Tears_of_the_Kingdom/ann/tears_of_the_kingdom_split_clips_36s_overlap18s_0.7-1.0_val.jsonl \
    --output_file DATA/ann/tears_of_the_kingdom_final_val.jsonl \
    --select_nums 60 120 60
# 771	1621	791
python -m proactvl.data.preprocess.post_preprocess --input_files \
    DATA/game_commentary/Yu_Gi_Oh/ann/yu_gi_oh_split_clips_36s_overlap18s_0.0-0.3_val.jsonl \
    DATA/game_commentary/Yu_Gi_Oh/ann/yu_gi_oh_split_clips_36s_overlap18s_0.3-0.7_val.jsonl \
    DATA/game_commentary/Yu_Gi_Oh/ann/yu_gi_oh_split_clips_36s_overlap18s_0.7-1.0_val.jsonl \
    --output_file DATA/ann/yu_gi_oh_final_val.jsonl \
    --select_nums 60 120 60
# 1864	1996	101
python -m proactvl.data.preprocess.post_preprocess --input_files \
    DATA/game_commentary/Minecraft/ann/minecraft_split_clips_36s_overlap18s_0.0-0.3_val.jsonl \
    DATA/game_commentary/Minecraft/ann/minecraft_split_clips_36s_overlap18s_0.3-0.7_val.jsonl \
    DATA/game_commentary/Minecraft/ann/minecraft_split_clips_60s_overlap30s_0.0-0.3_val.jsonl \
    DATA/game_commentary/Minecraft/ann/minecraft_split_clips_60s_overlap30s_0.3-0.7_val.jsonl \
    --output_file DATA/ann/minecraft_final_val.jsonl \
    --select_nums 120 120 120 120

# python -m proactvl.data.preprocess.post_preprocess --input_files \
#     DATA/ego4d/v2/ann/ego4d_split_clips_60s_overlap30s_0.0-0.3_val.jsonl \
#     DATA/ego4d/v2/ann/ego4d_split_clips_60s_overlap30s_0.3-0.7_val.jsonl \
#     DATA/ego4d/v2/ann/ego4d_split_clips_60s_overlap30s_0.7-1.0_val.jsonl \
#     --output_file DATA/ann/ego4d_final_val.jsonl \
#     --select_nums '-1' '-1' '-1'

# ======================livecc==============================
 python -m proactvl.data.preprocess.prepare_for_training_livecc --ann_dir DATA/live_sft/videos --output_file DATA/ann/livecc_final_train.jsonl --min_duration 18 --max_duration 60 --num_workers 16

# =========================== Special cases ==========================


# Special construction for ego4d val
python -m proactvl.data.preprocess.post_preprocess_for_ego4d_val --input_files \
    DATA/ego4d/v2/ann/ego4d_split_clips_300s_overlap0s_0.0-0.0_val.jsonl \
    DATA/ego4d/v2/ann/ego4d_split_clips_300s_overlap0s_0.0-1.0_val.jsonl \
    --output_file DATA/ann/ego4d_final_val.jsonl \
    --select_nums '-1' '-1'

# Special construction for soccernet val
python -m proactvl.data.preprocess.preprocess_for_soccernet

python -m proactvl.data.preprocess.prepare_for_training --ann_dir DATA/soccernet/ann \
    --clip_duration 36 --clip_overlap 18 --min_duration 18 --history_duration 60 --min_active_rate 0.0 --max_active_rate 0.0 --dataset_type_list val test
python -m proactvl.data.preprocess.prepare_for_training --ann_dir DATA/soccernet/ann \
    --clip_duration 36 --clip_overlap 18 --min_duration 18 --history_duration 60 --min_active_rate 0.0 --max_active_rate 0.3 --dataset_type_list val test
python -m proactvl.data.preprocess.prepare_for_training --ann_dir DATA/soccernet/ann \
    --clip_duration 36 --clip_overlap 18 --min_duration 18 --history_duration 60 --min_active_rate 0.3 --max_active_rate 0.7 --dataset_type_list val test
python -m proactvl.data.preprocess.prepare_for_training --ann_dir DATA/soccernet/ann \
    --clip_duration 36 --clip_overlap 18 --min_duration 18 --history_duration 60 --min_active_rate 0.7 --max_active_rate 1.0 --dataset_type_list val test

python -m proactvl.data.preprocess.summary --ann_dir DATA/soccernet/ann

python -m proactvl.data.preprocess.post_preprocess --input_files \
    DATA/soccernet/ann/soccernet_split_clips_36s_overlap18s_0.0-0.3_test.jsonl \
    DATA/soccernet/ann/soccernet_split_clips_36s_overlap18s_0.3-0.7_test.jsonl \
    DATA/soccernet/ann/soccernet_split_clips_36s_overlap18s_0.7-1.0_test.jsonl \
    DATA/soccernet/ann/soccernet_split_clips_36s_overlap18s_0.0-0.3_val.jsonl \
    DATA/soccernet/ann/soccernet_split_clips_36s_overlap18s_0.3-0.7_val.jsonl \
    DATA/soccernet/ann/soccernet_split_clips_36s_overlap18s_0.7-1.0_val.jsonl \
    --output_file DATA/ann/soccernet_final_val.jsonl \
    --select_nums 30 60 30 30 60 30

# merge val script
python -m proactvl.data.preprocess.merge_final