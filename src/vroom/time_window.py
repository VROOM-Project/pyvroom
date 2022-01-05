"""Time window for when a delivery/pickup/task is possible."""
from __future__ import annotations
from typing import Any, Sequence, Union

import numpy

from . import _vroom

MAX_VAL = numpy.iinfo(numpy.uint32).max


class TimeWindow(_vroom.TimeWindow):
    """Time window for when a delivery/pickup/task is possible.

    Relative values, e.g. `[0, 14400]` for a 4 hours time window starting at
    the beginning of the planning horizon. In that case all times reported in
    output with the arrival key are relative to the start of the planning
    horizon;

    Supprt the following features:

    * No arguments implies no time constraints.
    * Equality operator `==` based on both start and end time are the same.
    * Normal compare operator `<, >, <=, >=` based on start time.
    * Shift `<<, >>` based on non-overlap intervals.
    * Contains `X in Y` based on if number/interval inside other interval.
    * Length `len(X)` give length of interval.
    * Falsy on no constrained interval.

    Attributes:
        start:
            Start point (inclusice) of the time window.
        end:
            End point (inclusive) of the time window.

    Args:
        start:
            Start point (inclusive) of the time window. In
            seconds from the starting time. Assumed `0 < start`.
        end:
            End point (inclusive) of the time window. In
            seconds from the starting time. Assumes `start < end`.

    Examples:
        >>> tw = vroom.TimeWindow(2200, 8800)
        >>> tw
        vroom.TimeWindow(2200, 8800)
        >>> tw.start, tw.end, len(tw)
        (2200, 8800, 6600)
        >>> 1000 in tw, 5000 in tw
        (False, True)

    """

    start: int
    end: int

    def __init__(
        self,
        start: Union[_vroom.TimeWindow, Sequence[int], int] = 0,
        end: int = MAX_VAL,
    ) -> None:
        assert isinstance(end, int)
        if isinstance(start, _vroom.TimeWindow):
            if end != MAX_VAL:
                raise TypeError("Only one arg when input is vroom.TimeWindow.")
            start, end = start.start, start.end
        if isinstance(start, Sequence):
            if end != MAX_VAL:
                raise TypeError("Only one arg when input is a sequence.")
            start, end = start
        _vroom.TimeWindow.__init__(self, start=start, end=end)

    def __bool__(self) -> bool:
        return self.start != 0 or self.end != MAX_VAL

    def __contains__(self, other: Union[_vroom.TimeWindow, int]) -> bool:
        if isinstance(other, int):
            return self._contains(other)
        return self.start < other.start and other.end < self.end

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, _vroom.TimeWindow):
            return self.start == other.start and self.end == other.end
        return NotImplemented

    def __le__(self, other: TimeWindow) -> bool:
        return self.start <= other.start

    def __lshift__(self, other: TimeWindow) -> bool:
        return self.end < other.start

    def __len__(self):
        return self._length

    def __repr__(self):
        args = f"{self.start}, {self.end}" if self else ""
        return f"vroom.{self.__class__.__name__}({args})"

    def __rshift__(self, other: TimeWindow) -> bool:
        return self.start > other.end
