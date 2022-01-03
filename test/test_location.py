import pytest
import vroom
from vroom import _vroom

LOC_INDEX0 = _vroom.Location(index=4)
LOC_INDEX1 = vroom.LocationIndex(4)
LOC_INDEX2 = vroom.Location(index=5)

LOC_COORDS0 = _vroom.Location(coords=[1, 2])
LOC_COORDS1 = vroom.LocationCoordinates([1, 2])
LOC_COORDS2 = vroom.Location(coords=[1, 3])

LOC_BOTH0 = _vroom.Location(index=4, coords=[1, 2])
LOC_BOTH1 = vroom.Location(index=4, coords=[1, 2])
LOC_BOTH2 = vroom.Location(5, [1, 3])


def test_location_subclass():
    assert isinstance(LOC_INDEX2, vroom.LocationIndex)
    assert not isinstance(LOC_INDEX2, vroom.LocationCoordinates)
    assert isinstance(LOC_COORDS2, vroom.LocationCoordinates)
    assert not isinstance(LOC_COORDS2, vroom.LocationIndex)
    assert isinstance(LOC_BOTH1, vroom.LocationIndex)
    assert isinstance(LOC_BOTH1, vroom.LocationCoordinates)


def test_init():
    assert isinstance(vroom.Location(LOC_INDEX0), vroom.LocationIndex)
    assert isinstance(vroom.Location(LOC_INDEX1), vroom.LocationIndex)
    assert isinstance(vroom.Location(LOC_INDEX2), vroom.LocationIndex)

    assert not isinstance(vroom.Location(LOC_INDEX0),
                          vroom.LocationCoordinates)
    assert not isinstance(vroom.Location(LOC_INDEX1),
                          vroom.LocationCoordinates)
    assert not isinstance(vroom.Location(LOC_INDEX2),
                          vroom.LocationCoordinates)

    assert not isinstance(vroom.Location(LOC_COORDS0), vroom.LocationIndex)
    assert not isinstance(vroom.Location(LOC_COORDS1), vroom.LocationIndex)
    assert not isinstance(vroom.Location(LOC_COORDS2), vroom.LocationIndex)

    assert isinstance(vroom.Location(LOC_COORDS0), vroom.LocationCoordinates)
    assert isinstance(vroom.Location(LOC_COORDS1), vroom.LocationCoordinates)
    assert isinstance(vroom.Location(LOC_COORDS2), vroom.LocationCoordinates)

    with pytest.raises(TypeError):
        vroom.LocationIndex(LOC_COORDS0)
    with pytest.raises(TypeError):
        vroom.LocationIndex(LOC_COORDS1)

    with pytest.raises(TypeError):
        vroom.LocationCoordinates(LOC_INDEX0)
    with pytest.raises(TypeError):
        vroom.LocationCoordinates(LOC_INDEX1)


def test_equality():
    assert LOC_INDEX0 == LOC_INDEX1
    assert LOC_INDEX0 != LOC_INDEX2
    assert LOC_INDEX1 != LOC_INDEX2

    assert LOC_COORDS0 == LOC_COORDS1
    assert LOC_COORDS0 != LOC_COORDS2
    assert LOC_COORDS1 != LOC_COORDS2

    assert LOC_BOTH0 == LOC_BOTH1
    assert LOC_BOTH0 != LOC_BOTH2
    assert LOC_BOTH1 != LOC_BOTH2

    assert LOC_COORDS1 != LOC_INDEX1
    assert LOC_COORDS2 != LOC_INDEX2

    assert LOC_BOTH1 == LOC_INDEX1
    assert LOC_BOTH1 == LOC_COORDS1
    assert LOC_BOTH1 != LOC_INDEX2
    assert LOC_BOTH1 != LOC_COORDS2

    assert LOC_BOTH2 != LOC_INDEX1
    assert LOC_BOTH2 != LOC_COORDS1
    assert LOC_BOTH2 == LOC_INDEX2
    assert LOC_BOTH2 == LOC_COORDS2
