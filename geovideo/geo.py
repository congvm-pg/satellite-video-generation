"""Geospatial helpers."""

from __future__ import annotations

import math
from dataclasses import dataclass

EARTH_RADIUS_M = 6_371_000


@dataclass(frozen=True)
class Coordinate:
    lat: float
    lon: float


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
