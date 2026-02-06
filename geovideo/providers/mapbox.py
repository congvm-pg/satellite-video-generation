"""Mapbox provider."""

from __future__ import annotations

from .base import MapProvider

MAPBOX = MapProvider(
    name="mapbox",
    tile_url_template="https://api.mapbox.com/styles/v1/{z}/{x}/{y}?access_token={token}",
)
