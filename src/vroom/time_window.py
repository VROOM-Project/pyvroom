"""Time window for when a delivery/pickup is possible."""
from typing import Optional, Sequence, Union
from _vroom import _TimeWindow


class TimeWindow(_TimeWindow):
    """Time window for when a delivery/pickup is possible.

    Attributes:
        start:
            Start point (inclusice) of the time window.
        end:
            End point (inclusive) of the time window.
        length:
            Length of the time interval.

    Examples:
        >>> tw = vroom.TimeWindow(4, 6)
        >>> tw
        vroom.TimeWindow(4, 6)
        >>> tw.start, tw.end, tw.length
        (4, 6, 2)
        >>> 10 in tw, 5 in tw
        (False, True)
    """

    def __init__(
        self,
        start: int = 0,
        end: Optional[int] = None,
    ) -> None:
        """Class initializer.

        Args:
            start:
                Start point (inclusice) of the time window. In
                seconds from the starting time.
            end:
                End point (inclusive) of the time window. In
                seconds from the starting time. If included, have `start < end`
        """
        kwargs = {"start": int(start)}
        if end is not None:
            assert start < end
            kwargs["end"] = int(end)
        _TimeWindow.__init__(self, **kwargs)

    @staticmethod
    def from_args(
        args: Union["TimeWindow", int, Sequence[int]],
    ) -> "TimeWindow":
        """Convenience constructor.

        Allows for short-hand construction.

        -----------  ------------------------------
        condition    initializer
        -----------  ------------------------------
        TimeWindow   start=args.start, end=args.end
        integer      start=args
        length == 2  start=args[0], end=args[1]
        -----------  ------------------------------

        Args:
            args:
                Input to interpret as start, end or TimeWindow pair.

        Examples:
            >>> vroom.TimeWindow.from_args([8, 16])
            vroom.TimeWindow(8, 16)
            >>> vroom.TimeWindow.from_args(TimeWindow(8, 16))
            vroom.TimeWindow(8, 16)

        """
        if isinstance(args, _TimeWindow):
            return TimeWindow(args.start, args.end)
        assert len(args) == 2
        return TimeWindow(*args)

    def __repr__(self):
        return f"vroom.{self.__class__.__name__}({self.start}, {self.end})"
