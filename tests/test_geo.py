from geovideo.geo import (
    Bounds,
    Coordinate,
    haversine_distance,
    interpolate,
    latlon_to_pixel,
    pixel_to_latlon,
    zoom_for_bounds,
)


def test_haversine_distance_equator():
    a = Coordinate(lat=0, lon=0)
    b = Coordinate(lat=0, lon=1)
    distance = haversine_distance(a, b)
    assert 110_000 < distance < 112_000


def test_interpolate_midpoint():
    a = Coordinate(lat=0, lon=0)
    b = Coordinate(lat=10, lon=20)
    mid = interpolate(a, b, 0.5)
    assert mid.lat == 5
    assert mid.lon == 10


def test_web_mercator_roundtrip():
    lat = 37.7749
    lon = -122.4194
    pixel = latlon_to_pixel(lat, lon, zoom=3)
    restored = pixel_to_latlon(pixel.x, pixel.y, zoom=3)
    assert abs(restored.lat - lat) < 1e-5
    assert abs(restored.lon - lon) < 1e-5


def test_zoom_for_bounds():
    bounds = Bounds(min_lat=34.0, min_lon=-123.0, max_lat=38.0, max_lon=-118.0)
    zoom = zoom_for_bounds(bounds, viewport_px=(1280, 720))
    assert zoom > 0
