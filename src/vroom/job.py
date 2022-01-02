from typing import List, Optional, Sequence, Set, Union

import vroom
import _vroom

from .location import Location
from .time_window import TimeWindow


class Job(_vroom._Job):
    """A job with deliver and/or pickup that has to be performed.

    Examples:
        >>> vroom.Job(0, [4., 5.], delivery=[4], pickup=[7])
        vroom.Job(0, [4.0, 5.0], delivery=[4], pickup=[7])
    """

    def __init__(
        self,
        id: int,
        location: Union[_vroom.Location, int, Sequence[float]],
        type: _vroom.JOB_TYPE = _vroom.JOB_TYPE.SINGLE,
        setup: int = 0,
        service: int = 0,
        delivery: vroom.Amount = vroom.Amount(),
        pickup: vroom.Amount = vroom.Amount(),
        skills: Optional[Set[int]] = None,
        priority: int = 0,
        time_windows: Optional[Sequence[TimeWindow]] = None,
        description: str = "",
    ) -> None:
        """
        Args:
            id:
                Job identifier number. Two jobs can not have the same
                identifier.
            type:
                The type of job that has to be performed.
            location:
                Location of the job. If iterger, value interpreted as an the
                column in duration matrix. If pair of numbers, value
                interpreted as longitude and latitude coordinates respectively.
            setup:
                The cost of preparing the vehicle before actually going out for
                a job.
            service:
                The time (in secondes) it takes to pick up/deliver shipment
                when at customer.
            delivery:
                An interger representation of how much is being carried to
                customer.
            pickup:
                An interger representation of how much is being carried back
                from customer.
            skills:
                Skills required to perform job. Only vehicles which satisfies
                all required skills (i.e. has at minimum all skills values
                required) are allowed to perform this job.
            priority:
                The job priority level, where 0 is the most
                important and 100 is the least important.
            time_windows:
                Windows for where service is allowed to begin.
                Defaults to have not restraints.
            description:
                Optional string descriping the job.
        """
        assert isinstance(id, int)
        kwargs = dict(
            id=id,
            location=location,
            type=type,
            setup=setup,
            service=service,
            delivery=delivery,
            pickup=pickup,
            skills=skills,
            priority=priority,
            time_windows=time_windows,
            description=description,
        )
        kwargs = {key: value for key, value in kwargs.items()
                  if value or key == "id"}
        self._kwargs = kwargs.copy()
        kwargs["location"] = Location(kwargs["location"])
        if time_windows is not None:
            kwargs["tws"] = [TimeWindow.from_args(tw)
                             for tw in kwargs.pop("time_windows")]
        assert isinstance(type, _vroom.JOB_TYPE)
        if type == _vroom.JOB_TYPE.SINGLE:
            kwargs["delivery"] = vroom.Amount(delivery)
            kwargs["pickup"] = vroom.Amount(pickup)
            del kwargs["type"]
            del self._kwargs["type"]
        elif type == _vroom.JOB_TYPE.DELIVERY:
            kwargs["delivery"] = vroom.Amount(delivery)
            assert "pickup" not in kwargs
        elif type == _vroom.JOB_TYPE.PICKUP:
            kwargs["pickup"] = vroom.Amount(pickup)
            assert "delivery" not in kwargs

        _vroom._Job.__init__(self, **kwargs)

    def __repr__(self) -> str:
        kwargs = {key: value for key, value in self._kwargs.items()
                  if value or key == "id"}
        id = kwargs.pop("id")
        location = kwargs.pop("location")
        args = ", ".join(f"{key}={value}" for key, value in kwargs.items())
        return f"vroom.{self.__class__.__name__}({id}, {location}, {args})"

    @property
    def location(self) -> Location:
        """
        The location where to go.

        Either by index (used with duration matrix) or
        by coordinate (used with map server).
        """
        return Location(self._location)

    @property
    def time_windows(self) -> List[TimeWindow]:
        """Time window for when job can be delivered."""
        return [TimeWindow.from_args(tw) for tw in self._kwargs.get("time_windows", [])]
