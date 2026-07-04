
import base64
import io

import torch
from PIL import Image
from typing import Optional, List, Dict, Any, Union, Iterable, Tuple


def frame_to_base64(frame, format: str = "JPEG") -> str:
    """Encode a single video frame into a base64 string (no data-uri prefix).

    Accepts a ``PIL.Image`` or a ``torch.Tensor`` shaped ``[C, H, W]`` as
    returned by ``qwen_omni_utils`` ``fetch_video``.
    """
    if isinstance(frame, torch.Tensor):
        arr = frame.detach().cpu()
        if arr.dtype != torch.uint8:
            arr = arr.clamp(0, 255).to(torch.uint8)
        # [C, H, W] -> [H, W, C]
        arr = arr.permute(1, 2, 0).numpy()
        image = Image.fromarray(arr).convert("RGB")
    elif isinstance(frame, Image.Image):
        image = frame.convert("RGB")
    else:
        raise TypeError(f"Unsupported frame type for base64 encoding: {type(frame)}")

    buffer = io.BytesIO()
    image.save(buffer, format=format)
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


def _split_words(text: str) -> List[str]:
    if text is None:
        return []
    cleaned = text.replace('\n', ' ').replace('<|im_end|>', ' ').strip()
    parts = [w for w in cleaned.split() if len(w) > 0]
    if len(parts) == 1 and any('\u4e00' <= ch <= '\u9fff' for ch in parts[0]):
        return [ch for ch in parts[0] if ch.strip()]
    return parts

def prune_cache_span(cache, start: int, end: int):
    """
    In-place remove sequence span [start, end) from DynamicCache (all layers).
    Only performs tensor slice+concat and seen_tokens correction.
    Caller must ensure alignment with text/positions.
    """

    num_layers = len(cache.layers)
    for i in range(num_layers):
        k = cache.layers[i].keys
        v = cache.layers[i].values
        # Common layout 1: [B, H, T, D]
        # FIXME, hard coding, for qwen 2.5 omni, cache shape: [B, H, Seq_len, D]

        k_new = torch.cat([k[:, :, :start, :], k[:, :, end:, :]], dim=2)
        v_new = torch.cat([v[:, :, :start, :], v[:, :, end:, :]], dim=2)

        cache.layers[i].keys = k_new
        cache.layers[i].values = v_new
    return cache