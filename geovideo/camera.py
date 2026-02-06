"""Camera primitives for GeoVideo."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .geo import Bounds, Coordinate, WorldCoordinate, latlon_to_world, world_to_latlon, zoom_for_bounds


@dataclass(frozen=True)
class Camera:
    position: Coordinate
    bearing: float = 0.0
    pitch: float = 0.0
    roll: float = 0.0
    fov: float = 45.0
    zoom: float = 0.0


def auto_frame(
    coordinates: Iterable[Coordinate],
    viewport_px: tuple[int, int],
    padding: float = 0.1,
    min_zoom: float = 0.0,
    max_zoom: float = 22.0,
) -> Camera:
    """Compute a camera that frames the provided coordinates."""

    bounds = Bounds.from_coordinates(coordinates)
    zoom = zoom_for_bounds(bounds, viewport_px, padding=padding)
    zoom = max(min_zoom, min(max_zoom, zoom))
    sw_world = latlon_to_world(bounds.min_lat, bounds.min_lon)
    ne_world = latlon_to_world(bounds.max_lat, bounds.max_lon)
    center_world = WorldCoordinate(
        x=(sw_world.x + ne_world.x) / 2,
        y=(sw_world.y + ne_world.y) / 2,
    )
    center = world_to_latlon(world=center_world)
    return Camera(position=center, zoom=zoom)
