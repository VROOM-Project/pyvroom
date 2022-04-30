from __future__ import annotations
from typing import List, Optional, Sequence, Set, Union

import numpy

from .amount import Amount
from .break_ import Break
from .input.vehicle_step import VehicleStep
from .location import Location, LocationCoordinates, LocationIndex
from .time_window import TimeWindow

from . import _vroom

MAX_VAL = int(numpy.iinfo(numpy.uintp).max)


class Vehicle(_vroom.Vehicle):
    """Vehicle for performing transport.

    Args:
        id:
            Vehicle idenfifier number. Two vehicle can not have the same
            identifier.
        start:
            The location where the vehicle starts at before any jobs are done.
            If omitted, the vehicle will start at the first task it will be
            assigned. If interger, value interpreted as an the column in
            duration matrix. If pair of numbers, value interpreted as longitude
            and latitude coordinates respectively.
        end:
            The location where the vehicle should end up after all jobs are
            completed. If omitted, the vehicle will end at the last task it
            will be assigned. If interger, value interpreted as an the column
            in duration matrix. If pair of numbers, value interpreted as
            longitude and latitude coordinates respectively.
        profile:
            The name of the profile this vehicle falls under.
        capacity:
            Array of intergers representing the capacity to carry different
            goods.
        skills:
            Skills provided by this vehilcle needed to perform various tasks.
        time_window:
            The time window for when this vehicle is available for usage.
        breaks:
            Breaks this vehicle should take.
        description:
            Optional string descriping the vehicle.
        speed_factor:
            The speed factor for which this vehicle runs faster or slower than
            the default.
        max_tasks:
            The maximum number of tasks this vehicle can perform.
        steps:
            Set of custom steps this vehicle should take.

    Examples:
        >>> vroom.Vehicle(1, end=1)
        vroom.Vehicle(1, end=1)

    """

    def __init__(
        self,
        id: int,
        start: Union[None, Location, int, Sequence[float]] = None,
        end: Union[None, Location, int, Sequence[float]] = None,
        profile: str = "car",
        capacity: Union[Amount, Sequence[int]] = (),
        skills: Optional[Set[int]] = None,
        time_window: Optional[TimeWindow] = None,
        breaks: Sequence[Break] = (),
        description: str = "",
        speed_factor: float = 1.0,
        max_tasks: int = MAX_VAL,
        steps: Sequence[VehicleStep] = (),
    ) -> None:
        self._speed_factor = float(speed_factor)
        _vroom.Vehicle.__init__(
            self,
            id=int(id),
            start=(None if start is None else Location(start)),
            end=(None if end is None else Location(end)),
            profile=str(profile),
            capacity=Amount(capacity),
            skills=(set([]) if skills is None else skills),
            time_window=(TimeWindow() if time_window is None else TimeWindow(time_window)),
            breaks=[Break(break_) for break_ in breaks],
            description=str(description),
            speed_factor=self._speed_factor,
            max_tasks=max_tasks,
            steps=[VehicleStep(step) for step in steps],
        )
        assert isinstance(self.capacity, Amount)

    def __repr__(self) -> str:
        args = [f"{self.id}"]
        if self.start is not None:
            if isinstance(self.start, Location):
                args.append(f"start={self.start}")
            elif isinstance(self.start, LocationIndex):
                args.append(f"start={self.start.index}")
            elif isinstance(self.start, LocationCoordinates):
                args.append(f"start={self.start.coords}")
        if self.end is not None:
            if isinstance(self.end, Location):
                args.append(f"end={self.end}")
            if isinstance(self.end, LocationIndex):
                args.append(f"end={self.end.index}")
            elif isinstance(self.end, LocationCoordinates):
                args.append(f"end={self.end.coords}")
        if self.profile != "car":
            args.append(f"profile={self.profile!r}")
        if self.capacity != Amount([]):
            args.append(f"capacity={numpy.asarray(self.capacity).tolist()}")
        if self.skills:
            args.append(f"skills={self.skills}")
        if self.time_window:
            args.append(f"time_window={self.time_window.start, self.time_window.end}")

        for name, default in [
            ("breaks", []),
            ("description", ""),
            ("speed_factor", 1.0),
            ("max_tasks", MAX_VAL),
            ("steps", []),
        ]:
            attribute = getattr(self, name)
            if attribute != default:
                args.append(f"{name}={attribute!r}")

        return f"vroom.{self.__class__.__name__}({', '.join(args)})"

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, value) -> None:
        self._id = value

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
        return [Break(break_) for break_ in self._breaks]

    @property
    def description(self) -> str:
        return self._description

    @property
    def speed_factor(self) -> float:
        return self._speed_factor

    @property
    def max_tasks(self) -> str:
        return self._max_tasks

    @property
    def steps(self) -> List[VehicleStep]:
        return [VehicleStep(step) for step in self._steps]

    def has_same_locations(self, vehicle: Vehicle) -> bool:
        return self._has_same_locations(vehicle)

    def has_same_profile(self, vehicle: Vehicle) -> bool:
        return self._has_same_profile(vehicle)
