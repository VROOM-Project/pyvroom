import numpy
import pytest

from vroom import _vroom
import vroom

MAX_VAL = numpy.iinfo(numpy.uint32).max


def test_time_window_init():
    tw = vroom.TimeWindow()
    assert tw.start == 0
    assert tw.end == MAX_VAL
    assert _vroom.TimeWindow().end == MAX_VAL

    with pytest.raises(_vroom.VroomInputException):
        vroom.TimeWindow(1000, 0)

    with pytest.raises(TypeError):
        vroom.TimeWindow(tw, 1000)

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
    assert not 50 in tw
    assert 150 in tw
    assert not 250 in tw

    assert vroom.TimeWindow(0, 150) not in tw
    assert vroom.TimeWindow(120, 180) in tw
    assert vroom.TimeWindow(120, 280) not in tw


def test_time_window_bool():
    assert vroom.TimeWindow(0, 100)
    assert not vroom.TimeWindow()
