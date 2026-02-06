"""OpenStreetMap provider."""

from __future__ import annotations

from .base import MapProvider

OSM = MapProvider(name="osm", tile_url_template="https://tile.openstreetmap.org/{z}/{x}/{y}.png")
