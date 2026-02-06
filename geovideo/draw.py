"""Rendering helpers."""

from __future__ import annotations

import importlib.util
from dataclasses import dataclass
from typing import Sequence

from .camera import Camera
from .geo import Coordinate, latlon_to_pixel


@dataclass(frozen=True)
class RenderFrame:
    frame_id: int
    camera: Camera


@dataclass(frozen=True)
class ImageLayer:
    image: "Image"
    position: tuple[int, int] = (0, 0)


@dataclass(frozen=True)
class TextLayer:
    text: str
    position: tuple[int, int]
    font_path: str | None = None
    font_size: int = 18
    color: tuple[int, int, int] = (255, 255, 255)


@dataclass(frozen=True)
class MarkerLayer:
    coordinate: Coordinate
    radius: int = 6
    color: tuple[int, int, int] = (255, 0, 0)


def _require_pillow():
    if importlib.util.find_spec("PIL") is None:
        raise RuntimeError("Pillow is required for rendering layers")
    from PIL import Image, ImageDraw, ImageFont

    return Image, ImageDraw, ImageFont


def _load_font(ImageFont, font_path: str | None, font_size: int) -> "ImageFont.FreeTypeFont":
    if font_path:
        return ImageFont.truetype(font_path, font_size)
    for candidate in (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ):
        from pathlib import Path

        if Path(candidate).exists():
            return ImageFont.truetype(candidate, font_size)
    return ImageFont.load_default()


def render_layers(
    size: tuple[int, int],
    layers: Sequence[ImageLayer | TextLayer | MarkerLayer],
    *,
    camera: Camera | None = None,
    background: tuple[int, int, int, int] = (0, 0, 0, 0),
) -> "Image":
    """Render layers into a PIL image."""

    Image, ImageDraw, ImageFont = _require_pillow()
    canvas = Image.new("RGBA", size, background)
    draw = ImageDraw.Draw(canvas)

    for layer in layers:
        if isinstance(layer, ImageLayer):
            canvas.alpha_composite(layer.image, layer.position)
        elif isinstance(layer, TextLayer):
            font = _load_font(ImageFont, layer.font_path, layer.font_size)
            draw.text(layer.position, layer.text, fill=layer.color, font=font)
        elif isinstance(layer, MarkerLayer):
            if camera is None:
                raise ValueError("camera is required for marker layers")
            pixel = latlon_to_pixel(layer.coordinate.lat, layer.coordinate.lon, camera.zoom)
            x = int(pixel.x)
            y = int(pixel.y)
            draw.ellipse(
                (x - layer.radius, y - layer.radius, x + layer.radius, y + layer.radius),
                fill=layer.color,
                outline=None,
            )

    return canvas


def render_frame(frame_id: int, camera: Camera) -> RenderFrame:
    """Return a representation of a rendered frame."""

    return RenderFrame(frame_id=frame_id, camera=camera)
