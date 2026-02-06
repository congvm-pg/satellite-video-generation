"""Mapbox provider."""

from __future__ import annotations

from .base import MapProvider

MAPBOX = MapProvider(
    name="mapbox",
    tile_url_template=(
        "https://api.mapbox.com/styles/v1/mapbox/streets-v11/tiles/256/"
        "{z}/{x}/{y}?access_token={token}"
    ),
    throttle_s=0.1,
    max_retries=4,
)
