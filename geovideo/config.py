"""Configuration helpers for GeoVideo projects."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ProjectConfig:
    """Runtime configuration for a GeoVideo project."""

    project_root: Path
    assets_dir: Path
    output_dir: Path

    @classmethod
    def from_root(cls, project_root: Path) -> "ProjectConfig":
        assets_dir = project_root / "geovideo" / "assets"
        output_dir = project_root / "output"
        return cls(project_root=project_root, assets_dir=assets_dir, output_dir=output_dir)
