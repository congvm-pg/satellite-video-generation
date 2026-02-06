"""Command-line entry point for GeoVideo."""

from __future__ import annotations

import json
import random
from pathlib import Path
from typing import Optional

import typer

from .camera import auto_frame
from .config import ProjectConfig
from .geo import Coordinate
from .schemas import CameraModel, CoordinateModel, Project

app = typer.Typer(help="GeoVideo project helper")


def _set_seed(seed: Optional[int]) -> None:
    if seed is not None:
        random.seed(seed)


def _load_project(path: Path) -> Project:
    data = json.loads(path.read_text(encoding="utf-8"))
    return Project.model_validate(data)


@app.command()
def render(
    project_file: Path = typer.Option(..., "--project", exists=True, help="Path to project JSON"),
    output: Path = typer.Option(Path("output.mp4"), "--output", help="Output video path"),
    seed: Optional[int] = typer.Option(None, help="Random seed for deterministic rendering"),
) -> None:
    """Render a project to a video file."""

    _set_seed(seed)
    project = _load_project(project_file)
    typer.echo(f"Rendering '{project.title}' to {output}")


@app.command()
def preview(
    project_file: Path = typer.Option(..., "--project", exists=True, help="Path to project JSON"),
    seed: Optional[int] = typer.Option(None, help="Random seed for deterministic rendering"),
) -> None:
    """Preview project metadata."""

    _set_seed(seed)
    project = _load_project(project_file)
    typer.echo(f"Previewing '{project.title}' with {len(project.scenes)} scenes")


@app.command()
def validate(
    project_file: Path = typer.Option(..., "--project", exists=True, help="Path to project JSON"),
) -> None:
    """Validate a project file against the schema."""

    project = _load_project(project_file)
    typer.echo(f"Project '{project.title}' is valid with {len(project.scenes)} scenes")


@app.command()
def demo(
    output: Path = typer.Option(Path("demo.json"), "--output", help="Output demo project JSON"),
) -> None:
    """Generate a demo project."""

    config = ProjectConfig.from_root(Path.cwd())
    coords = [Coordinate(lat=37.7749, lon=-122.4194), Coordinate(lat=34.0522, lon=-118.2437)]
    camera = auto_frame(coords, viewport_px=(1280, 720))
    project = Project(
        title="Demo",
        scenes=[],
        camera=CameraModel(position=CoordinateModel(lat=camera.position.lat, lon=camera.position.lon), zoom=camera.zoom),
    )
    output.write_text(project.model_dump_json(indent=2), encoding="utf-8")
    typer.echo(f"Demo project written to {output} (assets dir: {config.assets_dir})")


def main() -> None:
    app()


if __name__ == "__main__":
    main()
