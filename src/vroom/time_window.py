"""Time window for when a delivery/pickup/task is possible."""

from __future__ import annotations
from typing import Any, Optional, Sequence, Union

from . import _vroom


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

    _start: int
    _end: int

    def __init__(
        self,
        start: Union[int, _vroom.TimeWindow, Sequence[int], None] = None,
        end: Optional[int] = None,
    ) -> None:
        if isinstance(start, _vroom.TimeWindow):
            if end is not None:
                raise TypeError("Only one arg when input is vroom.TimeWindow.")
            if start._is_default():
                start = end = None
            else:
                end = _vroom.scale_to_user_duration(start._end)
                start = _vroom.scale_to_user_duration(start._start)
        elif isinstance(start, Sequence):
            if end is not None:
                raise TypeError("Only one arg when input is a sequence.")
            start, end = start
        if (start is None) != (end is None):
            raise TypeError("Either none or both start and end has to be provided")
        if start is None:
            _vroom.TimeWindow.__init__(self)
        else:
            _vroom.TimeWindow.__init__(self, start=start, end=end)

    @property
    def start(self):
        return _vroom.scale_to_user_duration(self._start)

    @property
    def end(self):
        return _vroom.scale_to_user_duration(self._end)

    def __len__(self) -> int:
        return self.end - self.start

    def __contains__(self, value: int) -> bool:
        return value >= self.start and value <= self.end

    def __bool__(self) -> bool:
        return not self._is_default()

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, _vroom.TimeWindow):
            return self.start == other.start and self.end == other.end
        return NotImplemented

    def __le__(self, other: TimeWindow) -> bool:
        return self.start <= other.start

    def __lshift__(self, other: TimeWindow) -> bool:
        return self.end < other.start

    def __repr__(self):
        args = "" if self._is_default() else f"{self.start}, {self.end}"
        return f"vroom.{self.__class__.__name__}({args})"

    def __rshift__(self, other: TimeWindow) -> bool:
        return self.start > other.end
