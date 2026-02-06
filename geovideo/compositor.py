"""Compositor utilities."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from .draw import RenderFrame


@dataclass(frozen=True)
class Composite:
    frames: Sequence[RenderFrame]


def compose(frames: Sequence[RenderFrame]) -> Composite:
    """Compose rendered frames into a composite container."""

    return Composite(frames=frames)
