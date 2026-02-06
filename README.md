# GeoVideo

GeoVideo is a lightweight Python toolkit for describing map-based video projects. It includes
utilities for geospatial math, camera framing, timelines, and provider metadata that can be
integrated into a rendering pipeline.

## Package layout

- `geovideo/` contains the core modules and provider definitions.
- `examples/` includes sample project manifests.
- `geovideo/assets/` is reserved for fonts, icons, and overlays.
- `tests/` contains unit tests for geospatial and timeline utilities.

## Quick start

```bash
python -m geovideo.cli --root .
```

## Testing

```bash
pytest
```
