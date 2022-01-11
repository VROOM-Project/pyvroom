from typing import Any, Dict, List, Optional, Sequence, Set, Union

import numpy

from . import _vroom

from .amount import Amount
from .location import Location, LocationCoordinates, LocationIndex
from .time_window import TimeWindow


class JobBaseclass(_vroom.Job):
    """Baseclass for all Job classes containing common attributes."""

    def _get_attributes(self) -> Dict[str, Any]:
        """Arguments to be used in repr view."""
        attributes: Dict[str, Any] = {
            "id": self.id,
            "location": self.location,
            "setup": self.setup,
            "service": self.service,
            "skills": self.skills,
            "priority": self.priority,
            "time_windows": self.time_windows,
            "description": self.description,
        }
        return attributes

    @property
    def description(self) -> str:
        return self._description

    @property
    def id(self) -> int:
        return self._id

    @property
    def location(self) -> Location:
        """
        The location where to go.

        Either by index (used with duration matrix) or
        by coordinate (used with map server).
        """
        return Location(self._location)

    @property
    def priority(self) -> int:
        return self._priority

    @property
    def service(self) -> int:
        return self._service

    @property
    def setup(self) -> int:
        return self._setup

    @property
    def skills(self) -> int:
        return self._skills

    @property
    def time_windows(self) -> List[TimeWindow]:
        """Time window for when job can be delivered."""
        return [TimeWindow(tw) for tw in self._time_windows]

    def __repr__(self) -> str:
        attributes = self._get_attributes()
        args = [f"{self.id}"]
        if isinstance(attributes["location"], LocationIndex):
            args.append(f"{self.location.index}")
        elif isinstance(attributes["location"], LocationCoordinates):
            args.append(f"{self.location.coords}")
        else:
            args.append(f"{self.location}")
        if attributes["setup"]:
            args.append(f"setup={attributes['setup']}")
        if attributes["service"]:
            args.append(f"service={attributes['service']}")
        if attributes.get("amount", False):
            args.append(f"amount={numpy.asarray(attributes['amount']).tolist()}")
        if attributes.get("delivery", False):
            args.append(f"delivery={numpy.asarray(attributes['delivery']).tolist()}")
        if attributes.get("pickup", False):
            args.append(f"pickup={numpy.asarray(attributes['pickup']).tolist()}")
        if attributes["skills"]:
            args.append(f"skills={attributes['skills']}")
        if attributes["priority"]:
            args.append(f"priority={attributes['priority']}")
        if attributes["time_windows"] != [TimeWindow()]:
            windows = [(tw.start, tw.end) for tw in attributes["time_windows"]]
            args.append(f"time_windows={windows}")
        if attributes["description"]:
            args.append(f"description={attributes['description']!r}")
        return f"vroom.{self.__class__.__name__}({', '.join(args)})"


class JobSingle(JobBaseclass):
    """A regular one-stop job with both a deliver and pickup that has to be performed.

    Args:
        id:
            Job identifier number. Two jobs can not have the same
            identifier.
        location:
            Location of the job. If interger, value interpreted as an the
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

    Examples:
        >>> vroom.JobSingle(0, [4., 5.], delivery=[4], pickup=[7])
        vroom.JobSingle(0, (4.0, 5.0), delivery=[4], pickup=[7])
    """

    def __init__(
        self,
        id: int,
        location: Union[Location, int, Sequence[float]],
        setup: int = 0,
        service: int = 0,
        delivery: Amount = Amount(),
        pickup: Amount = Amount(),
        skills: Optional[Set[int]] = None,
        priority: int = 0,
        time_windows: Sequence[TimeWindow] = (),
        description: str = "",
    ) -> None:
        _vroom.Job.__init__(
            self,
            id=int(id),
            location=Location(location),
            setup=int(setup),
            service=int(service),
            delivery=Amount(delivery),
            pickup=Amount(pickup),
            skills=set(skills or []),
            priority=int(priority),
            tws=[TimeWindow(tw) for tw in time_windows] or [TimeWindow()],
            description=str(description),
        )

    @property
    def delivery(self) -> Amount:
        return Amount(self._delivery)

    @property
    def pickup(self) -> Amount:
        return Amount(self._pickup)

    def _get_attributes(self) -> Dict[str, Any]:
        """Arguments to be used in repr view."""
        attributes = super()._get_attributes()
        if self._pickup:
            attributes["pickup"] = self.pickup
        if self._delivery:
            attributes["delivery"] = self.delivery
        return attributes


class JobDelivery(JobBaseclass):
    """A delivery job that has to be performed.

    Args:
        id:
            Job identifier number. Two jobs can not have the same
            identifier.
        location:
            Location of the job. If interger, value interpreted as an the
            column in duration matrix. If pair of numbers, value
            interpreted as longitude and latitude coordinates respectively.
        setup:
            The cost of preparing the vehicle before actually going out for
            a job.
        service:
            The time (in secondes) it takes to pick up/deliver shipment
            when at customer.
        amount:
            An interger representation of how much is being carried to
            customer.
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

    Examples:
        >>> vroom.JobDelivery(0, [4., 5.], amount=[4])
        vroom.JobDelivery(0, (4.0, 5.0), amount=[4])
    """

    def __init__(
        self,
        id: int,
        location: Union[Location, int, Sequence[float]],
        setup: int = 0,
        service: int = 0,
        amount: Amount = Amount(),
        skills: Optional[Set[int]] = None,
        priority: int = 0,
        time_windows: Sequence[TimeWindow] = (),
        description: str = "",
    ) -> None:
        _vroom.Job.__init__(
            self,
            id=int(id),
            type=_vroom.JOB_TYPE.DELIVERY,
            location=Location(location),
            setup=int(setup),
            service=int(service),
            amount=Amount(amount),
            skills=set(skills or []),
            priority=int(priority),
            tws=[TimeWindow(tw) for tw in time_windows] or [TimeWindow()],
            description=str(description),
        )

    @property
    def amount(self) -> Amount:
        return Amount(self._delivery)

    def _get_attributes(self) -> Dict[str, Any]:
        """Arguments to be used in repr view."""
        attributes = super()._get_attributes()
        attributes["amount"] = self.amount
        return attributes


class JobPickup(JobBaseclass):
    """A pickup job that has to be performed.

    Args:
        id:
            Job identifier number. Two jobs can not have the same
            identifier.
        location:
            Location of the job. If interger, value interpreted as an the
            column in duration matrix. If pair of numbers, value
            interpreted as longitude and latitude coordinates respectively.
        setup:
            The cost of preparing the vehicle before actually going out for
            a job.
        service:
            The time (in secondes) it takes to pick up/deliver shipment
            when at customer.
        amount:
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

    Examples:
        >>> vroom.JobPickup(0, [4., 5.], amount=[7])
        vroom.JobPickup(0, (4.0, 5.0), amount=[7])
    """

    def __init__(
        self,
        id: int,
        location: Union[Location, int, Sequence[float]],
        setup: int = 0,
        service: int = 0,
        amount: Amount = Amount(),
        skills: Optional[Set[int]] = None,
        priority: int = 0,
        time_windows: Sequence[TimeWindow] = (),
        description: str = "",
    ) -> None:
        _vroom.Job.__init__(
            self,
            id=int(id),
            type=_vroom.JOB_TYPE.PICKUP,
            location=Location(location),
            setup=int(setup),
            service=int(service),
            amount=Amount(amount),
            skills=set(skills or []),
            priority=int(priority),
            tws=[TimeWindow(tw) for tw in time_windows] or [TimeWindow()],
            description=str(description),
        )

    @property
    def amount(self) -> Amount:
        return Amount(self._pickup)

    def _get_attributes(self) -> Dict[str, Any]:
        """Arguments to be used in repr view."""
        attributes = super()._get_attributes()
        attributes["amount"] = self.amount
        return attributes


class Job(JobSingle, JobDelivery, JobPickup):
    """A job with deliver and/or pickup that has to be performed.

    Args:
        id:
            Job identifier number. Two jobs can not have the same
            identifier.
        location:
            Location of the job. If interger, value interpreted as an the
            column in duration matrix. If pair of numbers, value
            interpreted as longitude and latitude coordinates respectively.
        setup:
            The cost of preparing the vehicle before actually going out for
            a job.
        service:
            The time (in secondes) it takes to pick up/deliver shipment
            when at customer.
        delivery:
            Array of intergers representing how much is being carried to
            customer.
        pickup:
            Array of intergers representing how much is being carried back from
            customer.
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

    Examples:
        >>> vroom.Job(0, [4., 5.], delivery=[4])
        vroom.JobDelivery(0, (4.0, 5.0), amount=[4])
        >>> vroom.Job(0, [4., 5.], pickup=[7])
        vroom.JobPickup(0, (4.0, 5.0), amount=[7])
        >>> vroom.Job(0, [4., 5.], delivery=[4], pickup=[7])
        vroom.JobSingle(0, (4.0, 5.0), delivery=[4], pickup=[7])

    """

    def __new__(
        cls,
        id: int,
        location: Union[Location, int, Sequence[float]],
        setup: int = 0,
        service: int = 0,
        delivery: Amount = Amount(),
        pickup: Amount = Amount(),
        skills: Optional[Set[int]] = None,
        priority: int = 0,
        time_windows: Sequence[TimeWindow] = (),
        description: str = "",
    ):
        kwargs = dict(
            id=int(id),
            location=Location(location),
            setup=setup,
            service=service,
            skills=skills or set([]),
            priority=priority,
            time_windows=[TimeWindow(tw) for tw in time_windows] or [TimeWindow()],
            description=description,
        )
        if delivery:
            if pickup:
                kwargs["delivery"] = delivery
                kwargs["pickup"] = pickup
                cls = JobSingle
            else:
                kwargs["amount"] = delivery
                cls = JobDelivery
        elif pickup:
            kwargs["amount"] = pickup
            cls = JobPickup
        else:
            cls = JobSingle

        instance = _vroom.Job.__new__(cls, **kwargs)
        instance.__init__(**kwargs)
        return instance

    # present to give correct help signature:
    def __init__(
        self,
        id: int,
        location: Union[Location, int, Sequence[float]],
        setup: int = 0,
        service: int = 0,
        delivery: Amount = Amount(),
        pickup: Amount = Amount(),
        skills: Optional[Set[int]] = None,
        priority: int = 0,
        time_windows: Sequence[TimeWindow] = (),
        description: str = "",
    ) -> None:
        """"""
        pass
