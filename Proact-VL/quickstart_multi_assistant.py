from proactvl.infer.multi_assistant_inference import MultiAssistantStreamInference

# config

"""
Currently the model release is under compliance review
and is restricted from public distribution.
Please send an email to the authors for a private share
of the model checkpoints.
"""
ckpt_path = 'oaaoaa/proactvl_base_qwen3vl'
model_config = None
infer_config = {
    'max_kv_tokens': 16384,
    'assistant_num': 2, # assistant number, initialize two assistants
    'enable_tts': False,
    'state_threshold': 0.5,
}
generate_config = {
    'do_sample': True,
    'max_new_tokens': 12,
    'temperature': 0.7,
    'top_p': 0.9,
    'repetition_penalty': 1.15,
}
talker_config = None
device_id = 0

# load model
stream_infer = MultiAssistantStreamInference(model_config, ckpt_path, infer_config, generate_config, talker_config, f'cuda:{device_id}')

# set system prompt 
system_prompt = ('You are a live commentator for a League of Legends (LoL) match. '
'Your role is to independently analyze and narrate the game, delivering insightful, engaging, and natural commentary just like a human expert.')
stream_infer.assistants[0].prime_system_prompt(system_prompt)
system_prompt_2 = 'You are a League of Legends play-by-play assistant, taking the role of supporting the main commentator during match commentary.'
stream_infer.assistants[1].prime_system_prompt(system_prompt_2)

video_path = './asset/sample.mp4'
video_begin = 0
video_end = 30
duration = video_end - video_begin
stream_infer.register_video_reader(video_path, video_begin, video_end)

overall_cc = {}
assistant_responses = None
for t in range(duration):
    current_second = video_begin + t
    history = ''
    user_query = ''
    assistant_responses, _ = stream_infer.infer_one_chunk(current_second, history=history, user_query=user_query, previous_responses=assistant_responses)
    for assistant_id in assistant_responses:
        assistant_response = assistant_responses[assistant_id]
        if assistant_response.active:
            commentary = assistant_response.commentary.strip()
            overall_cc[current_second] = commentary if assistant_response is not None else ''
            print(f'[Sec: {current_second}({assistant_response.score})] Assistant {assistant_id}: {commentary}')
        else:
            print(f'[Sec: {current_second}({assistant_response.score})] Assistant {assistant_id}: <|SILENCE|>')

# print('Final Commentary:', overall_cc)


