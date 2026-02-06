"""GeoVideo package for assembling map-based video projects."""

from __future__ import annotations

import importlib.util

from .config import ProjectConfig

__all__ = ["Project", "ProjectConfig"]
__version__ = "0.1.0"


def __getattr__(name: str):
    if name == "Project":
        if importlib.util.find_spec("pydantic") is None:
            raise AttributeError("Project requires pydantic to be installed")
        from .schemas import Project

        return Project
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
