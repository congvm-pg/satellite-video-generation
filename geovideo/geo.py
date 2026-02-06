"""Geospatial helpers."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Iterable

EARTH_RADIUS_M = 6_371_000
TILE_SIZE = 256
MAX_LAT = 85.05112878


@dataclass(frozen=True)
class Coordinate:
    lat: float
    lon: float


@dataclass(frozen=True)
class PixelCoordinate:
    x: float
    y: float


@dataclass(frozen=True)
class WorldCoordinate:
    x: float
    y: float


@dataclass(frozen=True)
class Bounds:
    min_lat: float
    min_lon: float
    max_lat: float
    max_lon: float

    @classmethod
    def from_coordinates(cls, coords: Iterable[Coordinate]) -> "Bounds":
        coords = list(coords)
        if not coords:
            raise ValueError("coords must not be empty")
        min_lat = min(c.lat for c in coords)
        max_lat = max(c.lat for c in coords)
        min_lon = min(c.lon for c in coords)
        max_lon = max(c.lon for c in coords)
        return cls(min_lat=min_lat, min_lon=min_lon, max_lat=max_lat, max_lon=max_lon)


def haversine_distance(a: Coordinate, b: Coordinate) -> float:
    """Return the great-circle distance in meters between two coordinates."""

    lat1 = math.radians(a.lat)
    lat2 = math.radians(b.lat)
    dlat = lat2 - lat1
    dlon = math.radians(b.lon - a.lon)
    hav = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 2 * EARTH_RADIUS_M * math.asin(math.sqrt(hav))


def interpolate(a: Coordinate, b: Coordinate, t: float) -> Coordinate:
    """Linearly interpolate between two coordinates."""

    if not 0 <= t <= 1:
        raise ValueError("t must be between 0 and 1")
    return Coordinate(lat=a.lat + (b.lat - a.lat) * t, lon=a.lon + (b.lon - a.lon) * t)


def clamp_lat(lat: float) -> float:
    return max(-MAX_LAT, min(MAX_LAT, lat))


def clamp_lon(lon: float) -> float:
    return max(-180.0, min(180.0, lon))


def latlon_to_world(lat: float, lon: float) -> WorldCoordinate:
    """Convert lat/lon to Web Mercator world coordinates in the range [0, 1]."""

    lat = clamp_lat(lat)
    lon = clamp_lon(lon)
    x = (lon + 180.0) / 360.0
    siny = math.sin(math.radians(lat))
    y = 0.5 - math.log((1 + siny) / (1 - siny)) / (4 * math.pi)
    return WorldCoordinate(x=x, y=y)


def world_to_latlon(world: WorldCoordinate) -> Coordinate:
    lon = world.x * 360.0 - 180.0
    n = math.pi - 2.0 * math.pi * world.y
    lat = math.degrees(math.atan(math.sinh(n)))
    return Coordinate(lat=lat, lon=lon)


def latlon_to_pixel(lat: float, lon: float, zoom: float) -> PixelCoordinate:
    """Convert lat/lon to pixel coordinates at a given zoom level."""

    world = latlon_to_world(lat, lon)
    scale = TILE_SIZE * 2**zoom
    return PixelCoordinate(x=world.x * scale, y=world.y * scale)


def pixel_to_latlon(x: float, y: float, zoom: float) -> Coordinate:
    scale = TILE_SIZE * 2**zoom
    world = WorldCoordinate(x=x / scale, y=y / scale)
    return world_to_latlon(world)


def zoom_for_bounds(bounds: Bounds, viewport_px: tuple[int, int], padding: float = 0.1) -> float:
    """Compute a zoom level that fits bounds into the viewport."""

    width_px, height_px = viewport_px
    if width_px <= 0 or height_px <= 0:
        raise ValueError("viewport_px must be positive")
    if padding < 0:
        raise ValueError("padding must be non-negative")
    sw = latlon_to_world(bounds.min_lat, bounds.min_lon)
    ne = latlon_to_world(bounds.max_lat, bounds.max_lon)
    span_x = max(ne.x - sw.x, 1e-9)
    span_y = max(sw.y - ne.y, 1e-9)
    span_x *= 1 + padding * 2
    span_y *= 1 + padding * 2
    zoom_x = math.log2(width_px / (TILE_SIZE * span_x))
    zoom_y = math.log2(height_px / (TILE_SIZE * span_y))
    return min(zoom_x, zoom_y)
