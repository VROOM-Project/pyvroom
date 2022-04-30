from __future__ import annotations
from typing import Sequence, Tuple, Union

from . import _vroom


class LocationIndex(_vroom.Location):
    """Index in the custom duration matrix for where to find distances.

    Attributes:
        index:
            Location index referring to column in the duration
            matrix.

    Args:
        index:
            Location index referring to column in the duration
            matrix.
        location:
            Other location with `index` attribute to make a copy of.

    Examples:
        >>> loc = LocationIndex(4)
        >>> loc
        vroom.LocationIndex(4)
        >>> loc.index
        4

    See also:
        :cls:`vroom.Location`

    """

    def __init__(
        self,
        index: Union[int, Location],
    ) -> None:
        if isinstance(index, _vroom.Location):
            if not index._user_index():
                name = index.__class__.__name__
                raise TypeError(f"Can not convert {name} to LocationIndex")
            index = index._index()
        _vroom.Location.__init__(self, index)
        assert not self._has_coordinates()

    @property
    def index(self) -> int:
        """Location index."""
        return self._index()

    def __repr__(self) -> str:
        return f"vroom.{self.__class__.__name__}({self.index})"


class LocationCoordinates(_vroom.Location):
    """Location longitude and latitude.

    Attributes:
        index:
            Location index referring to column in the duration
            matrix.
        coords:
            Longitude and latitude coordinate.

    Args:
        coords:
            Longitude and latitude coordinate.
        location:
            Other location with `coords` attribute to make a copy of.

    Examples:
        >>> loc = LocationCoordinates([2., 3.])
        >>> loc
        vroom.LocationCoordinates((2.0, 3.0))
        >>> loc.coords
        (2.0, 3.0)

    See also:
        :cls:`vroom.Location`

    """

    def __init__(
        self,
        coords: Union[Location, Sequence[float]],
    ) -> None:
        if isinstance(coords, _vroom.Location):
            if not coords._has_coordinates():
                name = coords.__class__.__name__
                raise TypeError(f"Can not convert {name} to LocationCoordinates")
            coords = [coords._lon(), coords._lat()]
        assert isinstance(coords, Sequence)
        coords = [float(coord) for coord in coords]
        assert len(coords) == 2
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

    Converts to :cls:`LocationCoordinates` if no `index` is provided, and to
    :cls:`LocationIndex` if not `coords` is provided.

    Attributes:
        index:
            Location index referring to column in the duration
            matrix.
        coords:
            Longitude and latitude coordinate.

    Args:
        index:
            Location index referring to column in the duration
            matrix.
        coords:
            Longitude and latitude coordinate.
        location:
            Other location to make a smart copy of.

    Examples:
        >>> loc = vroom.Location(index=4, coords=(7., 8.))
        >>> loc
        vroom.Location(index=4, coords=(7.0, 8.0))
        >>> loc.index, loc.coords
        (4, (7.0, 8.0))
        >>> vroom.Location(4)
        vroom.LocationIndex(4)
        >>> vroom.Location((7., 8.))
        vroom.LocationCoordinates((7.0, 8.0))

    See also:
        :cls:`vroom.LocationIndex`, :cls:`vroom.LocationCoordinates`

    """

    __init__ = _vroom.Location.__init__

    def __new__(
        cls,
        *args,
        **kwargs,
    ):
        if len(args) + len(kwargs) > 2:
            raise TypeError("too many arguents in input.")
        if args and "index" in kwargs:
            raise TypeError("index reference twice.")

        illegal_kwargs = False
        if len(args) == 2:
            illegal_kwargs = bool(kwargs)
            kwargs["index"], kwargs["coords"] = args
        elif len(args) == 1:
            if isinstance(args[0], _vroom.Location):
                illegal_kwargs = bool(kwargs)
                if args[0]._user_index():
                    kwargs["index"] = args[0]._index()
                if args[0]._has_coordinates():
                    kwargs["coords"] = [args[0]._lon(), args[0]._lat()]

            elif isinstance(args[0], Sequence):
                illegal_kwargs = bool(kwargs)
                kwargs["coords"] = args[0]

            else:
                kwargs["index"] = args[0]

        if illegal_kwargs:
            raise TypeError("too many arguents in input.")

        kwargs = {
            key: list(value) if isinstance(value, Sequence) else value for key, value in kwargs.items()
        }

        if cls is Location and len(kwargs) == 1:
            cls = LocationIndex if "index" in kwargs else LocationCoordinates
            instance = _vroom.Location.__new__(cls, **kwargs)
            instance.__init__(**kwargs)
        else:
            instance = _vroom.Location.__new__(cls, **kwargs)
        return instance

    def __repr__(self) -> str:
        args = f"index={self.index}, coords={self.coords}"
        return f"vroom.{self.__class__.__name__}({args})"
