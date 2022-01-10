from __future__ import annotations
from typing import List, Sequence, Union

from .time_window import TimeWindow
from . import _vroom


class Break(_vroom.Break):
    """A break allocated to the vehicle's driver.

    Args:
        id:
            Job identifier number. Two jobs can not have the
            same identifier.
        time_windows:
            Time windows for where breaks is allowed to begin.
            Defaults to have not restraints.
        service:
            The time duration (in secondes) of the break.
        description:
            A string describing this break.

    Examples:
        >>> vroom.Break(id=4, time_windows=[vroom.TimeWindow(0, 1000)], service=200, description="lunch")
        vroom.Break(4, time_windows=[(0, 1000)], service=200, description='lunch')
    """

    def __init__(
        self,
        id: Union[Break, int],
        time_windows: Sequence[TimeWindow] = (),
        service: int = 0,
        description: str = "",
    ) -> None:
        if isinstance(id, _vroom.Break):
            assert time_windows == ()
            assert service == 0
            assert description == ""
            time_windows = id._time_windows
            service = id._service
            description = id._description
            id = id._id
        _vroom.Break.__init__(
            self,
            id=id,
            time_windows=[TimeWindow(tw) for tw in time_windows],
            service=service,
            description=description,
        )

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, value: int) -> None:
        self._id = value

    @property
    def time_windows(self) -> List[TimeWindow]:
        return [TimeWindow(tw) for tw in self._time_windows]

    @time_windows.setter
    def time_windows(self, value: Sequence[TimeWindow]) -> None:
        self._time_windows = [TimeWindow(tw) for tw in value]

    @property
    def service(self) -> int:
        return self._service

    @service.setter
    def service(self, value: int) -> None:
        self._service = value

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        self._description = value

    def is_valid_start(self, time: int):
        return self._is_valid_start(time=time)

    def __repr__(self) -> str:
        args = [f"{self.id}"]
        if self.time_windows:
            args.append(f"time_windows={[(tw.start, tw.end) for tw in self.time_windows]}")
        if self.service:
            args.append(f"service={self.service}")
        if self.description:
            args.append(f"description={self.description!r}")
        return f"vroom.{self.__class__.__name__}({', '.join(args)})"
