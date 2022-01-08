from typing import List, Optional, Sequence, Set, Union

from .amount import Amount
from .break_ import Break
from .location import Location
from .time_window import TimeWindow
from .input.vehicle_step import VehicleStep

from . import _vroom


class Vehicle(_vroom.Vehicle):
    """Vehicle for performing transport.

    Examples:
        >>> vehicle = Vehicle(1, end=1)
        >>> vehicle
        vroom.Vehicle(1, end=1, profile='car')
    """

    def __init__(
        self,
        id: int,
        start: Union[None, Location, int, Sequence[float]] = None,
        end: Union[None, Location, int, Sequence[float]] = None,
        profile: str = "car",
        capacity: Amount = Amount(),
        skills: Optional[Set[int]] = None,
        time_window: Optional[TimeWindow] = None,
        breaks: Sequence[Break] = (),
        description: str = "",
        speed_factor: Optional[float] = None,
        max_tasks: Optional[int] = None,
        input_steps: Sequence[VehicleStep] = (),
    ) -> None:
        kwargs = dict(
            id=id,
            start=start,
            end=end,
            profile=profile,
            capacity=Amount(capacity),
            skills=skills,
            time_window=time_window,
            breaks=breaks,
            description=description,
            speed_factor=speed_factor,
            max_tasks=max_tasks,
            input_steps=input_steps,
        )
        kwargs = {key: value for key, value in kwargs.items() if value or key == "id"}
        self._kwargs = kwargs.copy()
        kwargs["start"] = None if start is None else Location(start)
        kwargs["end"] = None if end is None else Location(end)
        if "time_window" in kwargs:
            kwargs["tw"] = kwargs.pop("time_window")
        _vroom.Vehicle.__init__(self, **kwargs)

    def __repr__(self) -> str:
        kwargs = {key: value for key, value in self._kwargs.items() if key == "id" or value}
        id = kwargs.pop("id")
        args = ", ".join(f"{key}={value!r}" for key, value in kwargs.items())
        return f"vroom.{self.__class__.__name__}({id}, {args})"

    @property
    def start(self) -> Optional[Location]:
        return Location(self._start) if self._start else None

    @property
    def end(self) -> Optional[Location]:
        return Location(self._end) if self._end else None

    @property
    def profile(self) -> str:
        return self._profile

    @property
    def capacity(self) -> Amount:
        return Amount(self._capacity)

    @property
    def skills(self) -> Set[int]:
        return self._skills

    @property
    def time_window(self) -> TimeWindow:
        return TimeWindow(self._time_window)

    @property
    def breaks(self) -> List[Break]:
        return Break(self._break)

    @property
    def description(self) -> str:
        return self._description

    @property
    def max_tasks(self) -> str:
        return self._max_tasks

    @property
    def steps(self) -> List[VehicleStep]:
        return [VehicleStep(step) for step in self._steps]
