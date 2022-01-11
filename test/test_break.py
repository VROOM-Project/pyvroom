import pytest
import vroom


def test_break_init():
    with pytest.raises(vroom._vroom.VroomInputException):
        vroom.Break(4)
    with pytest.raises(vroom._vroom.VroomInputException):
        vroom.Break(4, service=500)

    break_ = vroom.Break(vroom.Break(4, [(0, 1000)], 500, "hello"))
    assert break_.id == 4
    assert break_.time_windows == [vroom.TimeWindow(0, 1000)]
    assert break_.service == 500
    assert break_.description == "hello"


def test_break_attributes():
    break_ = vroom.Break(4, [(0, 1000), (2000, 3000)])
    assert break_.is_valid_start(500)
    assert not break_.is_valid_start(1500)
    assert break_.is_valid_start(2500)

    break_.id = 7
    assert break_.id == 7

    break_.time_windows = [(1000, 2000)]
    assert break_.time_windows == [vroom.TimeWindow(1000, 2000)]

    break_.service = 9
    assert break_.service == 9

    break_.description = "goodbye"
    assert break_.description == "goodbye"
