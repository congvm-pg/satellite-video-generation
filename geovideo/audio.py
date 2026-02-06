"""Audio helpers for GeoVideo."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class AudioTrack:
    name: str
    samples: Sequence[float]


def mix(tracks: Sequence[AudioTrack]) -> AudioTrack:
    """Mix audio tracks by averaging samples."""

    if not tracks:
        return AudioTrack(name="mix", samples=())
    length = max(len(track.samples) for track in tracks)
    mixed = []
    for i in range(length):
        values = [track.samples[i] for track in tracks if i < len(track.samples)]
        mixed.append(sum(values) / len(values))
    return AudioTrack(name="mix", samples=mixed)
