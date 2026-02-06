"""Schema definitions for GeoVideo projects."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Sequence

from .camera import Camera
from .timeline import Keyframe


@dataclass(frozen=True)
class Scene:
    name: str
    camera_path: Sequence[Keyframe]


@dataclass(frozen=True)
class Project:
    title: str
    scenes: Sequence[Scene] = field(default_factory=tuple)
    camera: Camera | None = None
