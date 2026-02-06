from geovideo.timeline import Keyframe, build_timeline


def test_build_timeline_interpolation():
    keyframes = [Keyframe(time_s=0, value=0), Keyframe(time_s=1, value=10)]
    timeline = build_timeline(keyframes, fps=2)
    assert timeline == [0, 5, 10]


def test_build_timeline_constant_after_end():
    keyframes = [Keyframe(time_s=0, value=3)]
    timeline = build_timeline(keyframes, fps=1)
    assert timeline == [3]
