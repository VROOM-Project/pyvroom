from _vroom import _Vehicle
from typing import List, Optional, Sequence, Set, Union

from .amount import Amount
from .break_ import Break
from .location import Location
from .time_window import TimeWindow
from .input.vehicle_step import VehicleStep


class Vehicle(_Vehicle):
    """Vehicle for performing transport.

    Examples:
        >>> vehicle = vroom.Vehicle(1, end=1)
        >>> vehicle
        vroom.Vehicle(1, end=1)
    """

    def __init__(
        self,
        id: int,
        start: Union[None, Location, int, Sequence[Union[int, float]]] = None,
        end: Union[None, Location, int, Sequence[Union[int, float]]] = None,
        profile: Optional[str] = None,
        capacity: int = 0,
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
            capacity=capacity,
            skills=skills,
            time_window=time_window,
            breaks=breaks,
            description=description,
            speed_factor=speed_factor,
            max_tasks=max_tasks,
            input_steps=input_steps,
        )
        kwargs = {key: value for key, value in kwargs.items()
                  if value or key == "id"}
        self._kwargs = kwargs.copy()
        kwargs["capacity"] = Amount(capacity)
        kwargs["start"] = None if start is None else Location.from_args(start)
        kwargs["end"] = None if end is None else Location.from_args(end)
        if "time_window" in kwargs:
            kwargs["tw"] = kwargs.pop("time_window")
        _Vehicle.__init__(self, **kwargs)

    def __repr__(self) -> str:
        kwargs = {key: value for key, value in self._kwargs.items()
                  if key == "id" or value}
        id = kwargs.pop("id")
        args = ", ".join(f"{key}={value!r}" for key, value in kwargs.items())
        return f"vroom.{self.__class__.__name__}({id}, {args})"

    @property
    def start(self) -> Optional[Location]:
        return Location.from_args(self._start) if self.has_start() else None

    @property
    def end(self) -> Optional[Location]:
        return Location.from_args(self._end) if self.has_end() else None

    @property
    def time_window(self) -> TimeWindow:
        return TimeWindow.from_args(self.tw)

    @property
    def input_steps(self) -> List[VehicleStep]:
        return [VehicleStep.from_args(step) for step in self.steps]
