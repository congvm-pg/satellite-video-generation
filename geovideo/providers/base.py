"""Provider interfaces."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MapProvider:
    name: str
    tile_url_template: str

    def tile_url(self, z: int, x: int, y: int) -> str:
        return self.tile_url_template.format(z=z, x=x, y=y)
