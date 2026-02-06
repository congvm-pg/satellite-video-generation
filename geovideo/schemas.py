"""Schema definitions for GeoVideo projects."""

from __future__ import annotations

from typing import Iterable, Sequence

from pydantic import BaseModel, Field, field_validator, model_validator

from .camera import Camera
from .geo import Coordinate

MAX_POIS = 50


class CoordinateModel(BaseModel):
    lat: float = Field(..., description="Latitude in degrees")
    lon: float = Field(..., description="Longitude in degrees")

    @field_validator("lat")
    @classmethod
    def validate_lat(cls, value: float) -> float:
        if not -90 <= value <= 90:
            raise ValueError("lat must be between -90 and 90")
        return value

    @field_validator("lon")
    @classmethod
    def validate_lon(cls, value: float) -> float:
        if not -180 <= value <= 180:
            raise ValueError("lon must be between -180 and 180")
        return value

    def to_coordinate(self) -> Coordinate:
        return Coordinate(lat=self.lat, lon=self.lon)


class POI(BaseModel):
    name: str
    location: CoordinateModel

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("name must not be empty")
        return cleaned


class CameraKeyframe(BaseModel):
    time_s: float
    position: CoordinateModel
    zoom: float = 0.0
    bearing: float = 0.0
    pitch: float = 0.0
    roll: float = 0.0
    fov: float = 45.0
    easing: str = "linear"

    def to_camera(self) -> Camera:
        return Camera(
            position=self.position.to_coordinate(),
            bearing=self.bearing,
            pitch=self.pitch,
            roll=self.roll,
            fov=self.fov,
            zoom=self.zoom,
        )


class CameraModel(BaseModel):
    position: CoordinateModel
    bearing: float = 0.0
    pitch: float = 0.0
    roll: float = 0.0
    fov: float = 45.0
    zoom: float = 0.0

    def to_camera(self) -> Camera:
        return Camera(
            position=self.position.to_coordinate(),
            bearing=self.bearing,
            pitch=self.pitch,
            roll=self.roll,
            fov=self.fov,
            zoom=self.zoom,
        )


class Scene(BaseModel):
    name: str
    camera_path: Sequence[CameraKeyframe]
    pois: Sequence[POI] = Field(default_factory=tuple)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("name must not be empty")
        return cleaned

    @model_validator(mode="after")
    def validate_pois(self) -> "Scene":
        if len(self.pois) > MAX_POIS:
            raise ValueError(f"pois must contain at most {MAX_POIS} entries")
        return self


class Project(BaseModel):
    title: str
    scenes: Sequence[Scene] = Field(default_factory=tuple)
    camera: CameraModel | None = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("title must not be empty")
        return cleaned

    def iter_pois(self) -> Iterable[POI]:
        for scene in self.scenes:
            yield from scene.pois
