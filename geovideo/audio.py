"""Audio helpers for GeoVideo."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence


@dataclass(frozen=True)
class AudioTrack:
    name: str
    samples: Sequence[float]
    sample_rate: int = 44_100


def apply_fade(samples: Sequence[float], sample_rate: int, fade_in_s: float, fade_out_s: float) -> list[float]:
    total = len(samples)
    fade_in_samples = int(sample_rate * fade_in_s)
    fade_out_samples = int(sample_rate * fade_out_s)
    result = list(samples)

    for i in range(min(fade_in_samples, total)):
        result[i] *= i / max(1, fade_in_samples)
    for i in range(min(fade_out_samples, total)):
        idx = total - 1 - i
        result[idx] *= i / max(1, fade_out_samples)
    return result


def duck_background(
    foreground: Sequence[float],
    background: Sequence[float],
    *,
    threshold: float = 0.1,
    duck_db: float = -8.0,
) -> list[float]:
    gain = 10 ** (duck_db / 20.0)
    length = max(len(foreground), len(background))
    ducked = []
    for i in range(length):
        fg = foreground[i] if i < len(foreground) else 0.0
        bg = background[i] if i < len(background) else 0.0
        if abs(fg) >= threshold:
            bg *= gain
        ducked.append(bg)
    return ducked


def mix(
    tracks: Sequence[AudioTrack],
    *,
    ducking: tuple[int, int] | None = None,
    fade_in_s: float = 0.0,
    fade_out_s: float = 0.0,
) -> AudioTrack:
    """Mix audio tracks with optional ducking and fades."""

    if not tracks:
        return AudioTrack(name="mix", samples=())

    sample_rate = tracks[0].sample_rate
    for track in tracks:
        if track.sample_rate != sample_rate:
            raise ValueError("All tracks must share the same sample rate")

    samples = [list(track.samples) for track in tracks]
    if ducking:
        fg_index, bg_index = ducking
        samples[bg_index] = duck_background(samples[fg_index], samples[bg_index])

    length = max(len(track) for track in samples)
    mixed = []
    for i in range(length):
        values = [track[i] for track in samples if i < len(track)]
        mixed.append(sum(values) / len(values))

    mixed = apply_fade(mixed, sample_rate, fade_in_s, fade_out_s)
    return AudioTrack(name="mix", samples=mixed, sample_rate=sample_rate)
