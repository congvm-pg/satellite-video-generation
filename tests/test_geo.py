from geovideo.geo import Coordinate, haversine_distance, interpolate


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
