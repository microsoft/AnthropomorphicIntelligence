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
    'temperature': 0.0,
}


def parse_args():
    parser = argparse.ArgumentParser(
        description="Distributed offline interleave-response generation over the game commentary val split"
    )
    parser.add_argument(
        "--model_name_or_path", type=str, required=True,
        help="OpenRouter model name, e.g., openai/gpt-4o-2024-11-20"
    )
    parser.add_argument(
        "--num_workers", type=int, default=1,
        help="Number of parallel processes to use"
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
    parser.add_argument(
        "--keep_turns", type=int, default=4,
        help="Number of most recent (frame, response) turns to keep as context"
    )
    parser.add_argument(
        "--max_tokens", type=int, default=64,
        help="Max output tokens per frame"
    )
    return parser.parse_args()


def build_interleave_prompt(system_prompt):
    """Append interleave-specific instructions to the base system prompt.

    In the interleave setting the model sees one frame at a time and must
    either produce a short piece of real-time commentary or stay silent.
    """
    return system_prompt.strip() + "\n\n" + (
        "You are watching the video one frame at a time. For each new frame, "
        "either produce a short piece of real-time commentary in English, or, "
        "if nothing noteworthy is happening, reply exactly with 'No reply'. "
        "Output plain text only, with no prefixes, labels, timestamps, or formatting."
    )


def generate_interleave_commentary(
    client,
    model_name_or_path,
    videos_b64_1fps,   # already a list of 1fps frames
    system_prompt='',
    keep_turns=4,
    max_tokens=64,
):
    """Run frame-by-frame interleave inference, keeping the most recent turns.

    Returns a list of per-frame results: [{"frame_idx": int, "assistant": str|None}, ...].
    """
    base_prompt = build_interleave_prompt(system_prompt)

    conversation_history = []  # [(user_msg, assistant_msg), ...]
    results = []
    for i, frame in enumerate(videos_b64_1fps):
        messages = [{"role": "system", "content": base_prompt}]

        # keep only the most recent `keep_turns` (frame, response) turns
        if conversation_history:
            start_idx = max(0, len(conversation_history) - keep_turns)
            for user_msg, assistant_msg in conversation_history[start_idx:]:
                messages.append(user_msg)
                messages.append(assistant_msg)

        current_user_msg = {
            "role": "user",
            "content": [{
                "type": "image_url",
                "image_url": {"url": "data:image/jpeg;base64," + frame},
            }],
        }
        messages.append(current_user_msg)

        # A single frame may fail (bad/truncated API response, rate limit, ...).
        # Skip only that frame instead of discarding the whole record.
        try:
            completion = client.chat.completions.create(
                model=model_name_or_path,
                messages=messages,
                max_tokens=max_tokens,
                **generate_config
            )
            assistant_content = (completion.choices[0].message.content or "").strip()
        except Exception as e:
            print(f'[frame {i}]: Raise error {e}')
            results.append({"frame_idx": i, "assistant": None})
            continue

        conversation_history.append(
            (current_user_msg, {"role": "assistant", "content": assistant_content})
        )

        assistant_or_none = assistant_content
        if not assistant_content or "No reply" in assistant_content:
            assistant_or_none = None
        results.append({"frame_idx": i, "assistant": assistant_or_none})

    return results


def interleave_worker(
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
        tag = record['tag']
        dataset_name = record['dataset_name']
        if dataset_name not in dataset_names:
            continue
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

        try:
            results = generate_interleave_commentary(
                client=client,
                model_name_or_path=model_name_or_path,
                videos_b64_1fps=videos_b64,
                system_prompt=system_prompt,
                keep_turns=args.keep_turns,
                max_tokens=args.max_tokens,
            )
        except Exception as e:
            print(f'[IDX: {idx}]: Raise error {e}')
            results = []

        # map each replied frame to its timestamp
        pred_dict = {}
        for item in results:
            if item['assistant'] is not None:
                timestamp = str(video_begin + item['frame_idx'])
                pred_dict[timestamp] = item['assistant']

        with open(save_path, 'w') as wf:
            json.dump({
                "video_id": video_path.split('/')[-1],
                "begin": video_begin,
                "end": video_end,
                "pred": pred_dict,
                "dataset_name": dataset_name,
                'tag': tag,
                'idx': data_uid
            }, wf, ensure_ascii=False)


if __name__ == "__main__":
    args = parse_args()
    multiprocessing.set_start_method('spawn', force=True)
    game_list_str = '_'.join(args.game_list)
    save_dir = os.path.join(args.output_dir, os.path.basename(args.model_name_or_path), game_list_str)

    worker_fn = partial(
        interleave_worker,
        model_name_or_path=args.model_name_or_path,
        save_dir=save_dir,
        num_workers=args.num_workers,
        args=args
    )
    local_mp(
        list(range(args.num_workers)),
        worker_fn,
        desc="interleave_generation",
        num_workers=args.num_workers
    )

    # jsons -> jsonl
    save_path = save_dir + '.jsonl'
    with open(save_path, 'w') as wf:
        for file in os.listdir(save_dir):
            datum = json.load(open(os.path.join(save_dir, file)))
            wf.write(json.dumps(datum) + '\n')
    # remove save_dir
    shutil.rmtree(save_dir)
