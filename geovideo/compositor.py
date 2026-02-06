"""Compositor utilities."""

from __future__ import annotations

import importlib.util
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

from .draw import RenderFrame


@dataclass(frozen=True)
class Composite:
    frames: Sequence[RenderFrame]


def _require_moviepy():
    if importlib.util.find_spec("moviepy") is None:
        raise RuntimeError("moviepy is required to encode videos")
    from moviepy.editor import ImageSequenceClip

    return ImageSequenceClip


def _require_numpy():
    if importlib.util.find_spec("numpy") is None:
        raise RuntimeError("numpy is required to encode videos")
    import numpy as np

    return np


def compose(frames: Sequence[RenderFrame]) -> Composite:
    """Compose rendered frames into a composite container."""

    return Composite(frames=frames)


def encode_video(
    frames: Iterable["Image"],
    output_path: Path,
    *,
    fps: int = 30,
    codec: str = "libx264",
) -> Path:
    """Encode PIL images into a video file."""

    ImageSequenceClip = _require_moviepy()
    np = _require_numpy()
    frame_list = [np.array(frame.convert("RGB")) for frame in frames]
    clip = ImageSequenceClip(frame_list, fps=fps)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    clip.write_videofile(str(output_path), codec=codec, audio=False, verbose=False, logger=None)
    return output_path
