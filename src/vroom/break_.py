from __future__ import annotations
from typing import List, Optional, Sequence, Union

import numpy

from .time_window import TimeWindow
from .amount import Amount
from . import _vroom


class Break(_vroom.Break):
    """A break allocated to the vehicle's driver.

    Examples:
        >>> vroom.Break(
        ...     id=4,
        ...     time_windows=[vroom.TimeWindow(0, 1000)],
        ...     service=200,
        ...     description="lunch",
        ...     max_load=[2, 3],
        ... )
        vroom.Break(4, time_windows=[(0, 1000)], service=200, description='lunch', max_load=[2, 3])
    """

    def __init__(
        self,
        id: Union[Break, int],
        time_windows: Sequence[TimeWindow] = (),
        service: int = 0,
        description: str = "",
        max_load: Union[None, Amount, Sequence[int]] = None,
    ) -> None:
        """
        Args:
            id:
                Job identifier number. Two jobs can not have the
                same identifier.
            time_windows:
                Time windows for where breaks is allowed to begin.
                Defaults to have not restraints.
            service:
                The time duration of the break.
            description:
                A string describing this break.
        """
        if isinstance(id, _vroom.Break):
            assert time_windows == ()
            assert service == 0
            assert description == ""
            assert max_load is None
            time_windows = id._time_windows
            service = _vroom.scale_to_user_duration(id._service)
            description = id._description
            max_load = id._max_load
            id = id._id
        _vroom.Break.__init__(
            self,
            id=id,
            time_windows=[TimeWindow(tw) for tw in time_windows],
            service=service,
            description=description,
            max_load=None if max_load is None else Amount(max_load),
        )

    @property
    def id(self) -> int:
        """Job identifier number. Two jobs can not have the same identifier."""
        return self._id

    @id.setter
    def id(self, value: int) -> None:
        self._id = value

    @property
    def time_windows(self) -> List[TimeWindow]:
        """Time windows for where breaks is allowed to begin."""
        return [TimeWindow(tw) for tw in self._time_windows]

    @time_windows.setter
    def time_windows(self, value: Sequence[TimeWindow]) -> None:
        self._time_windows = [TimeWindow(tw) for tw in value]

    @property
    def service(self) -> int:
        """The time duration of the break."""
        return _vroom.scale_to_user_duration(self._service)

    @service.setter
    def service(self, value: int) -> None:
        self._service = _vroom.scale_from_user_duration(value)

    @property
    def description(self) -> str:
        """A string describing this break."""
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        self._description = value

    @property
    def max_load(self) -> Optional[Amount]:
        """The maximum load the vehicle is allowed during the break."""
        return self._max_load

    @max_load.setter
    def max_load(self, value: Union[None, Amount, Sequence[int]]) -> None:
        self._max_load = None if value is None else Amount(value)

    def is_valid_start(self, time: int):
        """Check if break has a valid start time."""
        return self._is_valid_start(time=_vroom.scale_from_user_duration(time))

    def __repr__(self) -> str:
        args = [f"{self.id}"]
        if self.time_windows:
            args.append(f"time_windows={[(tw.start, tw.end) for tw in self.time_windows]}")
        if self.service:
            args.append(f"service={self.service}")
        if self.description:
            args.append(f"description={self.description!r}")
        if self.max_load:
            args.append(f"max_load={[int(load) for load in numpy.asarray(self.max_load)]}")
        return f"vroom.{self.__class__.__name__}({', '.join(args)})"
