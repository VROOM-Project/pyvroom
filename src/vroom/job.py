from typing import List, Optional, Sequence, Set, Union

from _vroom import _Job, JOB_TYPE

from .amount import Amount
from .location import Location
from .time_window import TimeWindow


class Job(_Job):
    """A job with deliver and/or pickup that has to be performed.

    Examples:
        >>> vroom.Job(0, [4., 5.], delivery=4, pickup=7)
        vroom.Job(0, [4.0, 5.0], delivery=4, pickup=7)
    """
    def __init__(
        self,
        id: int,
        location: Union[Location, int, Sequence[Union[int, float]]],
        type: JOB_TYPE = JOB_TYPE.SINGLE,
        setup: int = 0,
        service: int = 0,
        delivery: Union[int, Amount] = 0,
        pickup: Union[int, Amount] = 0,
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
                column in duration matrix. If pair of floats, value interpreted
                as longitude and latitude coordinates respectively. If a
                triplet, it is interpreted as `(index, longitude, latitude)`.
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
        assert isinstance(pickup, int)
        assert isinstance(delivery, int)
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
        kwargs["location"] = Location.from_args(location)
        if time_windows is not None:
            kwargs["tws"] = [TimeWindow.from_args(tw)
                             for tw in kwargs.pop("time_windows")]
        assert isinstance(type, JOB_TYPE)
        if type == JOB_TYPE.SINGLE:
            kwargs["delivery"] = Amount(delivery)
            kwargs["pickup"] = Amount(pickup)
            del kwargs["type"]
            del self._kwargs["type"]
        elif type == JOB_TYPE.DELIVERY:
            kwargs["delivery"] = Amount(delivery)
            assert "pickup" not in kwargs
        elif type == JOB_TYPE.PICKUP:
            kwargs["pickup"] = Amount(pickup)
            assert "delivery" not in kwargs

        _Job.__init__(self, **kwargs)

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
        return Location.from_args(self._kwargs["location"])

    @property
    def time_windows(self) -> List[TimeWindow]:
        """Time window for when job can be delivered."""
        return [TimeWindow.from_args(tw) for tw in self._kwargs.get("time_windows", [])]
