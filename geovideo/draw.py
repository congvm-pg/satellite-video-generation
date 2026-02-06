"""Rendering helpers."""

from __future__ import annotations

from dataclasses import dataclass

from .camera import Camera


@dataclass(frozen=True)
class RenderFrame:
    frame_id: int
    camera: Camera


def render_frame(frame_id: int, camera: Camera) -> RenderFrame:
    """Return a representation of a rendered frame."""

    return RenderFrame(frame_id=frame_id, camera=camera)
