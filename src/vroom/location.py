from typing import Optional, Sequence, Tuple, Union
from _vroom import _Location


class Location(_Location):
    """Location for where a job needs to e done.

    Either as an index referring to a column in the durations
    matrix, or as longitude-latitude coordinates.

    Attributes:
        index:
            Location index referring to column in the duration
            matrix.
        coords:
            Longitude and latitude coordinate.

    Examples:
        >>> vroom.Location(index=4)
        vroom.Location(index=4)
        >>> loc = vroom.Location(coords=(7., 8.))
        >>> loc.coords
        (7.0, 8.0)

    """

    def __init__(
            self,
            index: Optional[int] = None,
            coords: Optional[Sequence[float]] = None,
    ) -> None:
        if index is None and coords is None:
            raise KeyError(
                "either `index` or `coords` (or both) must be provided.")

        kwargs = {}
        if index is not None:
            assert isinstance(index, int)
            kwargs["index"] = index
        if coords is not None:
            assert isinstance(coords, Sequence)
            assert len(coords) == 2
            kwargs["coords"] = tuple(float(coord) for coord in coords)
        self._kwargs = kwargs
        _Location.__init__(self, **kwargs)

    def __repr__(self):
        args = ", ".join(f"{key}={value}"
                         for key, value in self._kwargs.items())
        return f"vroom.{self.__class__.__name__}({args})"

    @staticmethod
    def from_args(
            args: Union["Location", int, Sequence[Union[int, float]]],
    ) -> "Location":
        """Convenience constructor.

        Allows for short-hand construction from type and length.

        -----------  ---------------------------------------------
        condition    initializer
        -----------  ---------------------------------------------
        Location     index=args.index, coords=[args.lat, args.lon]
        integer      index=args
        length == 1  index=args[0]
        length == 2  coords=args
        length == 3  index=args[0], coords=args[1:]
        -----------  ---------------------------------------------

        Args:
            args:
                Input to interpret as index, coordinate or
                (index, coordinate) pair.

        Examples:
            >>> vroom.Location.from_args(1)
            vroom.Location(index=1)
            >>> vroom.Location.from_args([3., 4.])
            vroom.Location(coords=(3.0, 4.0))
            >>> vroom.Location.from_args([1, 3., 4.])
            vroom.Location(index=1, coords=(3.0, 4.0))
            >>> vroom.Location.from_args(Location(1, coords=[3., 5.]))
            vroom.Location(index=1, coords=(3.0, 5.0))
        """
        if isinstance(args, _Location):
            kwargs = dict(index=args._index())
            if args.has_coordinates():
                kwargs["coords"] = [args.lon(), args.lat()]
            return Location(**kwargs)
        if isinstance(args, int):
            return Location(index=args)
        assert 0 < len(args) < 4
        if len(args) == 1:
            return Location(index=args[0])
        if len(args) == 2:
            return Location(coords=args)
        return Location(index=args[0], coords=args[1:])

    @property
    def index(self) -> Optional[int]:
        """Location index.

        Examples:
            >>> loc = vroom.Location(4)
            >>> loc.index
            4
            >>> loc.index = 7
            >>> loc.index
            7
        """
        return self._index()

    @index.setter
    def index(self, value: int) -> None:
        assert isinstance(value, int)
        self.set_index(value)

    @property
    def coords(self) -> Optional[Tuple[float, float]]:
        """Location longitude and latitude coordinates.

        Examples:
            >>> vroom.Location(coords=[4, 5]).coords
            (4.0, 5.0)
            >>> vroom.Location(index=3).coords is None
            True

        """
        if self.has_coordinates():
            return self.lon(), self.lat()
        return None
