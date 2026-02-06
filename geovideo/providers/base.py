"""Provider interfaces."""

from __future__ import annotations

import hashlib
import time
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class TileCache:
    root: Path

    def path_for(self, z: int, x: int, y: int) -> Path:
        return self.root / str(z) / str(x) / f"{y}.png"

    def get(self, z: int, x: int, y: int) -> bytes | None:
        path = self.path_for(z, x, y)
        if path.exists():
            return path.read_bytes()
        return None

    def set(self, z: int, x: int, y: int, data: bytes) -> Path:
        path = self.path_for(z, x, y)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return path


@dataclass
class MapProvider:
    name: str
    tile_url_template: str
    throttle_s: float = 0.1
    max_retries: int = 3
    backoff_base_s: float = 0.5
    user_agent: str = "GeoVideo/0.1"
    _last_request_time: float = field(default=0.0, init=False, repr=False)

    def tile_url(self, z: int, x: int, y: int, token: str | None = None, **kwargs: str) -> str:
        format_args: dict[str, str | int] = {"z": z, "x": x, "y": y, **kwargs}
        if "{token}" in self.tile_url_template:
            if token is None:
                raise ValueError(f"Token required for provider '{self.name}'.")
            format_args["token"] = token
        return self.tile_url_template.format(**format_args)

    def fetch_tile(
        self,
        z: int,
        x: int,
        y: int,
        *,
        token: str | None = None,
        cache: TileCache | None = None,
        headers: dict[str, str] | None = None,
        **kwargs: Any,
    ) -> bytes:
        if cache:
            cached = cache.get(z, x, y)
            if cached is not None:
                return cached

        url = self.tile_url(z, x, y, token=token, **{k: str(v) for k, v in kwargs.items()})
        tile = self._request_with_retry(url, headers=headers)
        if cache:
            cache.set(z, x, y, tile)
        return tile

    def _request_with_retry(self, url: str, headers: dict[str, str] | None = None) -> bytes:
        for attempt in range(self.max_retries + 1):
            self._throttle()
            request_headers = {"User-Agent": self.user_agent}
            if headers:
                request_headers.update(headers)
            request = urllib.request.Request(url, headers=request_headers)
            try:
                with urllib.request.urlopen(request, timeout=15) as response:
                    data = response.read()
            except Exception:
                if attempt >= self.max_retries:
                    raise
                sleep_s = self.backoff_base_s * (2**attempt)
                time.sleep(sleep_s)
                continue
            return data
        raise RuntimeError("Failed to fetch tile")

    def _throttle(self) -> None:
        now = time.monotonic()
        elapsed = now - self._last_request_time
        if elapsed < self.throttle_s:
            time.sleep(self.throttle_s - elapsed)
        self._last_request_time = time.monotonic()


def cache_key(provider: MapProvider) -> str:
    hasher = hashlib.sha256()
    hasher.update(provider.name.encode("utf-8"))
    hasher.update(provider.tile_url_template.encode("utf-8"))
    return hasher.hexdigest()[:12]
