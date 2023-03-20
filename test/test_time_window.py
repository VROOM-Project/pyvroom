import pytest

from vroom import _vroom
import vroom


def test_time_window_init():
    tw = vroom.TimeWindow()
    assert tw.start == 0

    with pytest.raises(_vroom.VroomInputException):
        vroom.TimeWindow(1000, 0)
    with pytest.raises(TypeError):
        vroom.TimeWindow(tw, 1000)
    with pytest.raises(TypeError):
        vroom.TimeWindow(1000)

    tw = vroom.TimeWindow(1000, 2000)
    assert tw.start == vroom.TimeWindow(tw).start
    assert tw.end == vroom.TimeWindow(tw).end


def test_time_window_compare():
    assert vroom.TimeWindow(50, 150) > vroom.TimeWindow(0, 100)
    assert vroom.TimeWindow(0, 100) < vroom.TimeWindow(50, 150)
    assert vroom.TimeWindow(50, 150) >= vroom.TimeWindow(0, 100)
    assert vroom.TimeWindow(0, 100) <= vroom.TimeWindow(50, 150)
    assert vroom.TimeWindow(0, 100) >= vroom.TimeWindow(0, 100)
    assert vroom.TimeWindow(0, 100) <= vroom.TimeWindow(0, 100)
    assert vroom.TimeWindow(0, 100) != vroom.TimeWindow(0, 200)
    assert vroom.TimeWindow(0, 100) == vroom.TimeWindow(0, 100)

    assert not (vroom.TimeWindow(50, 150) < vroom.TimeWindow(0, 100))
    assert not (vroom.TimeWindow(0, 100) > vroom.TimeWindow(50, 150))
    assert not (vroom.TimeWindow(50, 150) <= vroom.TimeWindow(0, 100))
    assert not (vroom.TimeWindow(0, 100) >= vroom.TimeWindow(50, 150))
    assert not (vroom.TimeWindow(0, 100) != vroom.TimeWindow(0, 100))


def test_time_window_shift():
    assert vroom.TimeWindow(0, 100) << vroom.TimeWindow(200, 300)
    assert vroom.TimeWindow(200, 300) >> vroom.TimeWindow(0, 100)
    assert not (vroom.TimeWindow(0, 100) << vroom.TimeWindow(50, 150))
    assert not (vroom.TimeWindow(0, 100) >> vroom.TimeWindow(50, 150))

    assert not (vroom.TimeWindow(0, 300) == vroom.TimeWindow(100, 200))
    assert not (vroom.TimeWindow(0, 300) << vroom.TimeWindow(100, 200))
    assert not (vroom.TimeWindow(0, 300) >> vroom.TimeWindow(100, 200))


def test_time_window_contains():
    tw = vroom.TimeWindow(100, 200)
    assert 50 not in tw
    assert 150 in tw
    assert 250 not in tw


def test_time_window_bool():
    assert vroom.TimeWindow(0, 100)
    assert not vroom.TimeWindow()


def test_time_window_str():
    assert str(vroom.TimeWindow()) == "vroom.TimeWindow()"
    assert str(vroom.TimeWindow(0, 100)) == "vroom.TimeWindow(0, 100)"
