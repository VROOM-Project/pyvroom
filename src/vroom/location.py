from __future__ import annotations
from typing import Sequence, Tuple, Union

from . import _vroom


class LocationIndex(_vroom.Location):
    """Index in the custom duration matrix for where to find distances.

    Examples:
        >>> loc = LocationIndex(4)
        >>> loc
        vroom.LocationIndex(4)
        >>> loc.index
        4

    See also:
        :class:`vroom.Location`

    """

    def __init__(
        self,
        index: Union[int, Location],
    ) -> None:
        """
        Args:
            index:
                Location index referring to column in the duration
                matrix.
            location:
                Other location with `index` attribute to make a copy of.
        """
        if isinstance(index, _vroom.Location):
            if not index._user_index():
                name = index.__class__.__name__
                raise TypeError(f"Can not convert {name} to LocationIndex")
            index = index._index()
        _vroom.Location.__init__(self, index)
        assert not self._has_coordinates()

    @property
    def index(self) -> int:
        """Location index referring to column in the duration matrix."""
        return self._index()

    def __repr__(self) -> str:
        return f"vroom.{self.__class__.__name__}({self.index})"


class LocationCoordinates(_vroom.Location):
    """Location longitude and latitude.

    Examples:
        >>> loc = LocationCoordinates([2., 3.])
        >>> loc
        vroom.LocationCoordinates((2.0, 3.0))
        >>> loc.coords
        (2.0, 3.0)

    See also:
        :class:`vroom.Location`

    """

    def __init__(
        self,
        coords: Union[Location, Sequence[float], _vroom.Coordinates],
    ) -> None:
        """
        Args:
            coords:
                Longitude and latitude coordinate.
        """
        if isinstance(coords, _vroom.Location):
            if not coords._has_coordinates():
                name = coords.__class__.__name__
                raise TypeError(f"Can not convert {name} to LocationCoordinates")
            coords = coords._coords
        elif isinstance(coords, Sequence):
            coords = _vroom.Coordinates(*coords)
        _vroom.Location.__init__(self, coords=coords)
        assert self._has_coordinates()
        assert not self._user_index()

    @property
    def coords(self) -> Tuple[float, float]:
        """Location longitude and latitude."""
        return self._lon(), self._lat()

    def __repr__(self):
        return f"vroom.{self.__class__.__name__}({self.coords})"


class Location(LocationIndex, LocationCoordinates):
    """Location for where a job needs to e done.

    Either as an index referring to a column in the durations matrix, or as
    longitude-latitude coordinates.

    Converts to :class:`LocationCoordinates` if no `index` is provided, and to
    :class:`LocationIndex` if not `coords` is provided.

    Examples:
        >>> loc = vroom.Location(index=4, coords=[7., 8.])
        >>> loc
        vroom.Location(index=4, coords=(7.0, 8.0))
        >>> loc.index, loc.coords
        (4, (7.0, 8.0))
        >>> vroom.Location(4)
        vroom.LocationIndex(4)
        >>> vroom.Location([7., 8.])
        vroom.LocationCoordinates((7.0, 8.0))

    See also:
        :class:`vroom.LocationIndex`, :class:`vroom.LocationCoordinates`

    """

    __init__ = _vroom.Location.__init__
    """
    Args:
        index:
            Location index referring to column in the duration
            matrix.
        coords:
            Longitude and latitude coordinate.
        location:
            Other location to make a smart copy of.
    """

    def __new__(
        cls,
        index: Union[None, int, Sequence[float], _vroom.Location, _vroom.Coordinates] = None,
        coords: Union[None, Sequence[float], _vroom.Coordinates] = None,
    ):
        if isinstance(index, (Sequence, _vroom.Coordinates)):
            if coords is not None:
                raise TypeError("coord can not be provided twice.")
            coords = index
            index = None
        elif isinstance(index, _vroom.Location):
            if index._has_coordinates():
                if coords is not None:
                    raise TypeError("coords can not be provided with Location.")
                coords = _vroom.Coordinates(index._lon(), index._lat())
            if index._user_index():
                index = index._index()
            else:
                index = None
        if isinstance(coords, Sequence):
            coords = _vroom.Coordinates(*[float(coord) for coord in coords])

        kwargs = {}
        if index is None:
            cls = LocationCoordinates
        else:
            kwargs["index"] = index
        if coords is None:
            cls = LocationIndex
        else:
            kwargs["coords"] = coords

        instance = _vroom.Location.__new__(cls, **kwargs)
        instance.__init__(**kwargs)
        return instance

    def __repr__(self) -> str:
        args = f"index={self.index}, coords={self.coords}"
        return f"vroom.{self.__class__.__name__}({args})"
