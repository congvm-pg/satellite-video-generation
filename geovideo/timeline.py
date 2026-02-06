"""Timeline utilities."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence


@dataclass(frozen=True)
class Keyframe:
    time_s: float
    value: float


def build_timeline(keyframes: Sequence[Keyframe], fps: int) -> list[float]:
    """Build a timeline of values by linear interpolation."""

    if fps <= 0:
        raise ValueError("fps must be positive")
    if not keyframes:
        return []
    sorted_frames = sorted(keyframes, key=lambda k: k.time_s)
    if sorted_frames[0].time_s < 0:
        raise ValueError("time_s must be non-negative")
    end_time = sorted_frames[-1].time_s
    total_frames = int(round(end_time * fps)) + 1
    timeline = []
    current_index = 0
    for frame in range(total_frames):
        t = frame / fps
        while (
            current_index + 1 < len(sorted_frames)
            and sorted_frames[current_index + 1].time_s <= t
        ):
            current_index += 1
        start = sorted_frames[current_index]
        if current_index + 1 < len(sorted_frames):
            end = sorted_frames[current_index + 1]
            span = end.time_s - start.time_s
            if span == 0:
                value = end.value
            else:
                ratio = (t - start.time_s) / span
                value = start.value + (end.value - start.value) * ratio
        else:
            value = start.value
        timeline.append(value)
    return timeline


def normalize_keyframes(keyframes: Iterable[Keyframe]) -> list[Keyframe]:
    """Normalize keyframes ensuring sorted order and non-negative times."""

    frames = sorted(keyframes, key=lambda k: k.time_s)
    if frames and frames[0].time_s < 0:
        raise ValueError("time_s must be non-negative")
    return frames
