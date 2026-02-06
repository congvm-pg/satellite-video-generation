# GeoVideo

GeoVideo is a lightweight Python toolkit for describing map-based video projects. It includes
utilities for geospatial math, camera framing, timelines, and provider metadata that can be
integrated into a rendering pipeline.

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

Optional test dependencies:

```bash
pip install -e ".[test]"
```

## FFmpeg requirement

GeoVideo's video pipeline relies on FFmpeg through MoviePy/OpenCV. Install FFmpeg and ensure it is
available on your `PATH`:

```bash
ffmpeg -version
```

If the command is not found, install FFmpeg via your system package manager (for example, `brew
install ffmpeg` on macOS or `sudo apt-get install ffmpeg` on Debian/Ubuntu).

## Provider setup

GeoVideo ships with provider definitions for OpenStreetMap (OSM) and Mapbox tiles.

- **OpenStreetMap**: No API key required, but you must follow the OSM Tile Usage Policy and include
  attribution in any rendered video.
- **Mapbox**: Requires an access token. Store it in a secure place (such as an environment variable)
  and pass it to the provider when requesting tiles.

Example usage inside your own pipeline:

```python
from geovideo.providers.mapbox import MAPBOX

url = MAPBOX.tile_url(z=12, x=656, y=1582, token=os.environ["MAPBOX_ACCESS_TOKEN"])
```

## Project JSON schema (example)

Project manifests are validated against `geovideo.schemas.Project`. At minimum you must provide a
`title`, a list of `scenes`, and each scene must include a `camera_path` with timestamped
keyframes.

```json
{
  "title": "Sample Flight",
  "scenes": [
    {
      "name": "Downtown glide",
      "camera_path": [
        {
          "time_s": 0,
          "position": {"lat": 37.7749, "lon": -122.4194},
          "zoom": 11.5,
          "bearing": 20,
          "pitch": 45
        },
        {
          "time_s": 4,
          "position": {"lat": 37.7842, "lon": -122.4094},
          "zoom": 12.3,
          "bearing": 40,
          "pitch": 50
        }
      ],
      "pois": [
        {
          "name": "SF City Hall",
          "location": {"lat": 37.7793, "lon": -122.4192}
        }
      ]
    }
  ],
  "camera": {
    "position": {"lat": 37.7749, "lon": -122.4194},
    "zoom": 11.0,
    "bearing": 0,
    "pitch": 35,
    "fov": 45
  }
}
```

A working sample is available at `examples/project.sample.json`.

## Usage

Minimal run (preview metadata):

```bash
python -m geovideo.cli preview --project examples/project.sample.json
```

Advanced run (render with deterministic seed and explicit output path):

```bash
python -m geovideo.cli render --project examples/project.sample.json --output output/sample.mp4 --seed 42
```

The render command above is a complete example that produces an output video file at
`output/sample.mp4` when your rendering backend is wired up.

## Troubleshooting

- **Fonts missing or text renders incorrectly**: Ensure required fonts are installed on the host.
  If your renderer expects custom fonts, place them under `geovideo/assets/` and point your
  rendering code at that directory.
- **Blank or missing map tiles**: Confirm network access, provider URLs, and cache directory
  permissions. Respect provider throttle settings to avoid dropped responses.
- **API limits (Mapbox or other paid providers)**: Check usage dashboards, add caching, and lower
  request rates by increasing tile cache reuse or raising the throttle interval.

## Map tile terms & attribution

You are responsible for complying with tile provider terms of service. At a minimum:

- **OpenStreetMap**: Include attribution such as “© OpenStreetMap contributors” in your output and
  follow the [OSM Tile Usage Policy](https://operations.osmfoundation.org/policies/tiles/).
- **Mapbox**: Follow Mapbox attribution and usage requirements described in the Mapbox Terms of
  Service. Include required attributions when using Mapbox-hosted styles.

Always review the latest provider terms before distributing rendered videos.

## Testing

```bash
pytest
```
