"""Camera primitives for GeoVideo."""

from __future__ import annotations

from dataclasses import dataclass

from .geo import Coordinate


@dataclass(frozen=True)
class Camera:
    position: Coordinate
    bearing: float = 0.0
    pitch: float = 0.0
    roll: float = 0.0
    fov: float = 45.0
