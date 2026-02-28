from typing import Any, Dict, List, Optional, Sequence, Set, Union

import numpy

from . import _vroom

from .amount import Amount
from .location import Location, LocationCoordinates, LocationIndex
from .time_window import TimeWindow


class JobBaseclass:
    """Baseclass for all Job classes containing common attributes."""

    _id: int
    _location: Location
    _default_setup: int
    _default_service: int
    _time_windows: Sequence[TimeWindow]
    _description: str
    _setup_per_type: dict[str, int]
    _service_per_type: dict[str, int]

    def _get_attributes(self) -> Dict[str, Any]:
        """Arguments to be used in repr view."""
        return {
            "id": self.id,
            "location": self.location,
            "default_setup": self.default_setup,
            "default_service": self.default_service,
            "time_windows": self.time_windows,
            "description": self.description,
            "setup_per_type": self.setup_per_type,
            "service_per_type": self.service_per_type,
        }

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
    def default_service(self) -> int:
        return _vroom.scale_to_user_duration(self._default_service)

    @property
    def default_setup(self) -> int:
        return _vroom.scale_to_user_duration(self._default_setup)

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
        if attributes["default_setup"]:
            args.append(f"default_setup={attributes['default_setup']}")
        if attributes["default_service"]:
            args.append(f"default_service={attributes['default_service']}")
        if attributes.get("amount", False):
            args.append(f"amount={numpy.asarray(attributes['amount']).tolist()}")
        if attributes.get("delivery", False):
            args.append(f"delivery={numpy.asarray(attributes['delivery']).tolist()}")
        if attributes.get("pickup", False):
            args.append(f"pickup={numpy.asarray(attributes['pickup']).tolist()}")
        if attributes["time_windows"] != [TimeWindow()]:
            windows = [(tw.start, tw.end) for tw in attributes["time_windows"]]
            args.append(f"time_windows={windows}")
        if attributes["description"]:
            args.append(f"description={attributes['description']!r}")
        if attributes["setup_per_type"]:
            args.append(f"setup_per_type={attributes['setup_per_type']}")
        if attributes["service_per_type"]:
            args.append(f"service_per_type={attributes['service_per_type']}")
        return f"vroom.{self.__class__.__name__}({', '.join(args)})"


class Job(_vroom.Job, JobBaseclass):
    """A regular one-stop job with both a deliver and pickup that has to be performed.

    Examples:
        >>> vroom.Job(0, [4.0, 5.0], delivery=[4], pickup=[7])
        vroom.Job(0, (4.0, 5.0), delivery=[4], pickup=[7])
    """

    def __init__(
        self,
        id: int,
        location: Union[Location, int, Sequence[float]],
        default_setup: int = 0,
        default_service: int = 0,
        delivery: Amount = Amount(),
        pickup: Amount = Amount(),
        skills: Optional[Set[int]] = None,
        priority: int = 0,
        time_windows: Sequence[TimeWindow] = (),
        description: str = "",
        setup_per_type: dict[str, int] | None = None,
        service_per_type: dict[str, int] | None = None,
    ) -> None:
        """
        Args:
            id:
                Job identifier number. Two jobs can not have the same
                identifier.
            location:
                Location of the job. If interger, value interpreted as an the
                column in duration matrix. If pair of numbers, value
                interpreted as longitude and latitude coordinates respectively.
            default_setup:
                The cost of preparing the vehicle before actually going out for
                a job.
            default_service:
                The time (in secondes) it takes to pick up/deliver shipment
                when at customer.
            delivery:
                The amount of how much is being carried to customer.
            pickup:
                The amount of how much is being carried back from customer.
            skills:
                Skills required to perform job. Only vehicles which satisfies
                all required skills (i.e. has at minimum all skills values
                required) are allowed to perform this job.
            priority:
                The job priority level, where 0 is the lowest priority
                and 100 is the highest priority.
            time_windows:
                Windows for where service is allowed to begin.
                Defaults to have not restraints.
            description:
                Optional string descriping the job.
            setup_per_type:
                Object mapping vehicle types to job setup duration values.
            service_per_type:
                Object mapping vehicle types to job service duration values.
        """
        if not pickup:
            if not delivery:
                pickup = Amount([])
                delivery = Amount([])
            else:
                pickup = Amount([0] * len(delivery))
        elif not delivery:
            delivery = Amount([0] * len(pickup))
        _vroom.Job.__init__(
            self,
            id=int(id),
            location=Location(location),
            default_setup=int(default_setup),
            default_service=int(default_service),
            delivery=Amount(delivery),
            pickup=Amount(pickup),
            skills=set(skills or []),
            priority=int(priority),
            tws=[TimeWindow(tw) for tw in time_windows] or [TimeWindow()],
            description=str(description),
            setup_per_type=setup_per_type or {},
            service_per_type=service_per_type or {},
        )

    @property
    def delivery(self) -> Amount:
        """The amount of how much is being carried to customer."""
        return Amount(self._delivery)

    @property
    def pickup(self) -> Amount:
        """The amount of how much is being carried back from customer."""
        return Amount(self._pickup)

    @property
    def skills(self) -> int:
        """Skills required to perform job."""
        return self._skills

    @property
    def priority(self) -> int:
        """The job priority level."""
        return self._priority

    def _get_attributes(self) -> Dict[str, Any]:
        """Arguments to be used in repr view."""
        attributes = super()._get_attributes()
        if self._pickup:
            attributes["pickup"] = self.pickup
        if self._delivery:
            attributes["delivery"] = self.delivery
        if self._skills:
            attributes["skills"] = self.skills
        if self._priority:
            attributes["priority"] = self.priority
        return attributes


class ShipmentStep(JobBaseclass):
    """A delivery job that has to be performed.

    Examples:
        >>> vroom.ShipmentStep(0, [4.0, 5.0])
        vroom.ShipmentStep(0, (4.0, 5.0))
    """

    def __init__(
        self,
        id: int,
        location: Union[Location, int, Sequence[float]],
        default_setup: int = 0,
        default_service: int = 0,
        time_windows: Sequence[TimeWindow] = (),
        description: str = "",
        setup_per_type: dict[str, int] | None = None,
        service_per_type: dict[str, int] | None = None,
    ) -> None:
        """
        Args:
            id:
                Job identifier number. Two jobs can not have the same
                identifier.
            location:
                Location of the job. If interger, value interpreted as an the
                column in duration matrix. If pair of numbers, value
                interpreted as longitude and latitude coordinates respectively.
            default_setup:
                The cost of preparing the vehicle before actually going out for
                a job.
            default_service:
                The time (in secondes) it takes to pick up/deliver shipment
                when at customer.
            time_windows:
                Windows for where service is allowed to begin.
                Defaults to have not restraints.
            description:
                Optional string descriping the job.
            setup_per_type:
                Object mapping vehicle types to job setup duration values.
            service_per_type:
                Object mapping vehicle types to job service duration values.
        """
        self._id = int(id)
        self._location = Location(location)
        self._default_setup = _vroom.scale_from_user_duration(int(default_setup))
        self._default_service = _vroom.scale_from_user_duration(int(default_service))
        self._time_windows = [TimeWindow(tw) for tw in time_windows] or [TimeWindow()]
        self._description = str(description)
        self._setup_per_type = setup_per_type or {}
        self._service_per_type = service_per_type or {}


class Shipment:
    """A shipment that has to be performed.

    Examples:
        >>> pickup = vroom.ShipmentStep(0, [4.0, 5.0])
        >>> delivery = vroom.ShipmentStep(1, [5.0, 4.0])
        >>> vroom.Shipment(
        ...     pickup, delivery, amount=[7]
        ... )  # doctest: +NORMALIZE_WHITESPACE
        vroom.Shipment(vroom.ShipmentStep(0, (4.0, 5.0)),
                       vroom.ShipmentStep(1, (5.0, 4.0)),
                       amount=[7])
    """

    def __init__(
        self,
        pickup: ShipmentStep,
        delivery: ShipmentStep,
        amount: Amount = Amount(),
        skills: Optional[Set[int]] = None,
        priority: int = 0,
    ) -> None:
        """
        Args:
            pickup:
                Description of the pickup part of the shipment.
            delivery:
                Description of the delivery part of the shipment.
            amount:
                An interger representation of how much is being carried back
                from customer.
            skills:
                Skills required to perform job. Only vehicles which satisfies
                all required skills (i.e. has at minimum all skills values
                required) are allowed to perform this job.
            priority:
                The job priority level, where 0 is the lowest priority
                and 100 is the highest priority.
        """
        self.pickup = pickup
        self.delivery = delivery
        self.amount = Amount(amount)
        self.skills = skills or set()
        self.priority = int(priority)

    def __repr__(self) -> str:
        args = [str(self.pickup), str(self.delivery)]
        if self.amount:
            args.append(f"amount={numpy.asarray(self.amount).tolist()}")
        if self.skills:
            args.append(f"skills={self.skills}")
        if self.priority:
            args.append(f"priority={self.priority}")
        return f"vroom.{self.__class__.__name__}({', '.join(args)})"
