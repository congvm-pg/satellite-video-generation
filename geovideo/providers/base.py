"""Provider interfaces."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MapProvider:
    name: str
    tile_url_template: str

    def tile_url(self, z: int, x: int, y: int, token: str | None = None, **kwargs: str) -> str:
        format_args: dict[str, str | int] = {"z": z, "x": x, "y": y, **kwargs}
        if "{token}" in self.tile_url_template:
            if token is None:
                raise ValueError(f"Token required for provider '{self.name}'.")
            format_args["token"] = token
        return self.tile_url_template.format(**format_args)
