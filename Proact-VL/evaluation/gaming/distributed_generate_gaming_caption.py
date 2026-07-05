import os
import json
import tqdm
import shutil
import argparse
import multiprocessing
from functools import partial
from datasets import load_dataset
from proactvl.utils.multiprocessor import local_mp
from proactvl.utils.proact_process import process_interleave_mm_info
from proactvl.utils.conversations import construct_val_system_prompt
from proactvl.utils.utils import frame_to_base64
from openai import OpenAI

BASE_DIR = './DATA'

generate_config = {
    'temperature': 0.7,
    'top_p': 0.9,
}
def parse_args():
    parser = argparse.ArgumentParser(
        description="Distributed offline caption generation over the LiveSports-3K CC split"
    )
    parser.add_argument(
        "--model_name_or_path", type=str, required=True,
        help="HuggingFace model path, e.g., Qwen/Qwen2.5-VL-7B-Instruct"
    )
    parser.add_argument(
        "--num_workers", type=int, default=1,
        help="Number of parallel processes/gpus to use"
    )
    parser.add_argument(
        "--output_dir", type=str,
        default="./results/baseline",
        help="Directory to write generated JSON outputs"
    )
    parser.add_argument(
        "--game_list", type=str, nargs='+', default=[
            'lol', 'csgo', 'black_myth_wukong', 'cyberpunk'
        ],
        help="List of games to evaluate on"
    )
    parser.add_argument(
        "--test_name", type=str, default="all_in_one",
        help="The validation set name in oaaoaa/game_commentary_val dataset"
    )
    return parser.parse_args()


def build_messages(frames_b64, fps, prompt_text):
    return [{
        "role": "user",
        "content": [
            {"type": "text", "text": f"These frames were taken sequentially from the video at {fps} fps."},
            *[
                {
                    "type": "image_url",
                    "image_url": {"url": "data:image/jpeg;base64," + frame},
                }
                for frame in frames_b64
            ],
            {"type": "text", "text": prompt_text},
        ],
    }]

def call_model(client, model_name_or_path, messages, ):
    completion = client.chat.completions.create(
        model=model_name_or_path,
        messages=messages,
        **generate_config
    )
    print(completion)
    return (completion.choices[0].message.content or "").strip()

def generate_solo_commentary(
    client,
    model_name_or_path,
    videos_b64_1fps,   # already a list of 1fps frames: 36 or 60 frames
    history='',
    system_prompt='',
    fps=1,

):
    base_prompt = system_prompt
    if history != '':
        base_prompt += f"\nHere is previous commentary of the video:\n\n{history}\n\n"
    base_prompt += ("Please continue to comment the video and provide real-time, insightful, "
    "and engaging commentary on visual content."
    "Output ONE single paragraph of continuous commentary text in English only, with no line breaks. "
    "Do not include any extra symbols, labels, timestamps, JSON, or formatting.")
    messages = build_messages(videos_b64_1fps, fps=fps, prompt_text=base_prompt)
    commentary = call_model(
        client, model_name_or_path, messages
    )
    return commentary

def generate_multi_commentary(
    client,
    model_name_or_path,
    videos_b64_1fps,   # already a list of 1fps frames: 36 or 60 frames
    history='',
    system_prompt='',
    current_commentary='',
    fps=1,
):
    base_prompt = system_prompt.strip() + "\n\n"

    base_prompt += (
        "You are generating the ASSISTANT's live commentary for the given video frames.\n"
        "In the context below, the ASSISTANT's previous lines are prefixed with [ASSISTANT].\n"
        "Other commentators' lines are prefixed with [SPEAKER_*] (there may be multiple speakers).\n"
        "Use the context only as reference. Do NOT repeat any speaker tags in your output.\n\n"
    )

    if history != '':
        base_prompt += (
            "Context: previous commentary (chronological order):\n"
            f"{history}\n\n"
        )

    if current_commentary != '':
        base_prompt += (
            "Context: other commentators' descriptions of the current video frames:\n"
            f"{current_commentary}\n\n"
        )

    base_prompt += (
        "Task: Write ONLY the ASSISTANT's fresh, original real-time commentary for the given video frames.\n"
        "- Focus on what is visible in the frames and what is happening now.\n"
        "- Do not quote or copy the context verbatim; avoid repeating others' wording.\n"
        "- Do not output any prefixes such as [ASSISTANT] or [SPEAKER_*].\n"
        "- Output ONE single paragraph in English only, with no line breaks.\n"
        "- Do not include any extra symbols, labels, timestamps, JSON, or formatting.\n"
    )

    messages = build_messages(videos_b64_1fps, fps=fps, prompt_text=base_prompt)
    commentary = call_model(client, model_name_or_path, messages)
    return commentary

def generate_guidance_commentary(
    client,
    model_name_or_path,
    videos_b64_1fps,   # already a list of 1fps frames: 36 or 60 frames
    history='',
    system_prompt='',
    current_commentary='',
    fps=1,
):
    base_prompt = system_prompt.strip() + "\n\n"

    base_prompt += (
        "You will generate the ASSISTANT's live commentary for the provided video frames.\n"
        "In the context below, the ASSISTANT's earlier lines are prefixed with [ASSISTANT], "
        "and the user's query is prefixed with [USER].\n"
        "Treat this context as reference only and do not repeat any of these tags in your output.\n\n"
    )

    if history != '':
        base_prompt += (
            "Context (previous commentary, in chronological order):\n"
            f"{history}\n\n"
        )

    if current_commentary != '':
        base_prompt += (
            "User query about the current video frames:\n"
            f"{current_commentary}\n\n"
        )

    base_prompt += (
        "Task: Write ONLY the ASSISTANT's fresh, original real-time guidance for the given video frames.\n"
        "- Provide actionable tutorial-style instructions and tips based on what is happening now.\n"
        "- Focus on what the player should do next (strategy, timing, positioning, priorities, mistakes to avoid).\n"
        "- Do not quote or copy the context verbatim; avoid reusing the same phrasing.\n"
        "- Do not output any prefixes such as [ASSISTANT] or [USER].\n"
        "- Output exactly ONE single paragraph in English, with no line breaks.\n"
        "- Do not include any extra symbols, labels, timestamps, JSON, or other formatting.\n"
    )

    messages = build_messages(videos_b64_1fps, fps=fps, prompt_text=base_prompt)
    commentary = call_model(client, model_name_or_path, messages)
    return commentary

def caption_worker(
    device_id: int,
    model_name_or_path: str,
    save_dir: str,
    num_workers: int,
    args
):

    dataset_names = args.game_list

    ds = load_dataset('oaaoaa/game_commentary_val', name=args.test_name, split='test')

    idxs = list(range(len(ds)))
    idxs_on_device = idxs[device_id::num_workers]

    # Prepare temporary save folder for this model
    os.makedirs(save_dir, exist_ok=True)
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.environ.get("OPENROUTER_API_KEY", "<OPENROUTER_API_KEY>"),
        max_retries=5,
    )
    for idx in tqdm.tqdm(idxs_on_device, desc=f"Device {device_id}", total=len(idxs_on_device)):
        save_path = os.path.join(save_dir, f"{idx}.json")
        if os.path.exists(save_path):
            continue

        record = ds[idx]
        video_path = os.path.join(os.path.expanduser(BASE_DIR), record['video_path'])
        duration = record['video_duration']
        video_begin = record['video_begin']
        data_uid = record['idx']
        video_end = record['video_end']
        anns = record['annotations']
        tag = record['tag']
        dataset_name = record['dataset_name']
        if dataset_name not in dataset_names:
            continue
        history = record['history'] if 'history' in record else ''
        active_speaker = record['active_speaker']
        current_commentary_list = []
        for ann in record['annotations']:
            current_speaker = ann['speaker']
            # active speaker's own commentary is skipped below
            if ann['speaker'] == 'user':
                text = ann['query']
            else:
                assert 'text' in ann, f"Annotation has no text field: {ann}"
                text = ann['text']

            if current_speaker == active_speaker['name']:
                continue
            if len(current_commentary_list) == 0:
                current_commentary_list.append({
                    'speaker': current_speaker,
                    'text': text
                })
            elif current_speaker == current_commentary_list[-1]['speaker']:
                current_commentary_list[-1]['text'] += ' ' + text
            else:
                current_commentary_list.append({
                    'speaker': current_speaker,
                    'text': text
                })
        current_commentary_list_new = []
        for commentary_item in current_commentary_list:
            if commentary_item['speaker']!=active_speaker['name']:
                current_commentary_list_new.append(f"[{commentary_item['speaker']}]: {commentary_item['text']}")
        
        current_commentary = '\n'.join(current_commentary_list_new)
        system_prompt = construct_val_system_prompt(dataset_name, tag, record['active_speaker']['persona'])
        vision_info = [
            {
                "role": "user",
                "content": [{
                    "type": "video",
                    "video": video_path,
                    "video_start": video_begin,
                    "video_end": video_end,
                    "nframes": duration * 2,
                    "min_pixels": 128 * 28 * 28,
                    "max_pixels": 384 * 28 * 28
                }]
            }
        ]

        audios, images, videos = process_interleave_mm_info(vision_info, False, return_video_kwargs=False)
        # convert videos to a list of base64 frames
        videos_b64 = []
        for frames in videos:
            videos_b64.append(frame_to_base64(frames[0]))
        print(f'video length: {len(videos_b64)}')

        ann_map = {}
        for i in range(duration):
            ann_map[video_begin] = None
        for one_ann in anns:
            begin_time = one_ann['start']
            ann_map[begin_time] = one_ann
        if dataset_name in ['cyberpunk_2077', 'starcraft2', 'baldurs_gate_3', 'elden_ring', 'tears_of_the_kingdom', 'soccernet', 'black_myth_wukong']:
            commentary = generate_solo_commentary(
                client=client,
                model_name_or_path=model_name_or_path,
                videos_b64_1fps=videos_b64,
                fps=1,
                history=history,
                system_prompt=system_prompt,
            )
        elif dataset_name in ['yu_gi_oh', 'lol', 'csgo', 'streetfighter6']:
            try:
                commentary = generate_multi_commentary(
                    client=client,
                    model_name_or_path=model_name_or_path,
                    videos_b64_1fps=videos_b64,
                    fps=1,
                    history=history,
                    system_prompt=system_prompt,
                    current_commentary=current_commentary
                )
            except Exception as e:
                print(f'[IDX: {idx}]: Raise error {e}')
                commentary = ''
        elif dataset_name in ['minecraft', 'ego4d']:
            try:
                if len(videos_b64) <= 50:
                    commentary = generate_guidance_commentary(
                        client=client,
                        model_name_or_path=model_name_or_path,
                        videos_b64_1fps=videos_b64,
                        fps=1,
                        history=history,
                        system_prompt=system_prompt,
                        current_commentary=current_commentary
                    )
                else:
                    commentary_parts = []
                    rolling_history = history or ""
                    chunk_size = 50  # process 50 frames per chunk
                    for start in range(0, len(videos_b64), chunk_size):
                        frames = videos_b64[start:start + chunk_size]

                        part = generate_guidance_commentary(
                            client=client,
                            model_name_or_path=model_name_or_path,
                            videos_b64_1fps=frames,  # 1fps frames of the current 50s segment
                            fps=1,
                            history=rolling_history,
                            system_prompt=system_prompt,
                            current_commentary=current_commentary
                        )

                        commentary_parts.append(part)

                        # append this segment's commentary to history for the next continuation
                        if rolling_history:
                            if current_commentary:
                                rolling_history += (' ' + current_commentary)
                            rolling_history = rolling_history + " " + part
                        else:
                            if current_commentary:
                                rolling_history = current_commentary + " " + part
                            else:
                                rolling_history = part

                    commentary = " ".join([p for p in commentary_parts if p])
            except Exception as e:
                print(f'[IDX: {idx}]: Raise error {e}')
                commentary = ''
        else:
            raise NotImplementedError(f"Dataset {dataset_name} not supported yet.")


        with open(save_path, 'w') as wf:
            json.dump({
                "video_id": video_path.split('/')[-1],
                "begin": video_begin,
                "end": video_end,
                "pred": commentary,
                "dataset_name": dataset_name,
                'tag': tag,
                'idx': data_uid
            }, wf, ensure_ascii=False)

if __name__ == "__main__":
    args = parse_args()
    multiprocessing.set_start_method('spawn', force=True)
    game_list_str = '_'.join(args.game_list)
    save_dir = os.path.join(args.output_dir, os.path.basename(args.model_name_or_path), game_list_str)
    if True:
        worker_fn = partial(
            caption_worker,
            model_name_or_path=args.model_name_or_path,
            save_dir=save_dir,
            num_workers=args.num_workers,
            args=args
        )
        local_mp(
            list(range(args.num_workers)),
            worker_fn,
            desc="caption_generation",
            num_workers=args.num_workers
        )
    else:
        caption_worker(
            device_id=0,
            model_name_or_path=args.model_name_or_path,
            save_dir=save_dir,
            num_workers=args.num_workers,
            args=args
        )
        
    # jsons -> jsonl
    save_path = save_dir + '.jsonl'
    with open(save_path, 'w') as wf:
        for file in os.listdir(save_dir):
            datum = json.load(open(os.path.join(save_dir, file))) 
            wf.write(json.dumps(datum) + '\n')
    # remove save_dir
    shutil.rmtree(save_dir)

# python -m evaluation.gaming.distributed_generate_gaming_caption --model_name_or_path openai/gpt-4o-2024-11-20 --game_list cyberpunk_2077 --num_workers 8