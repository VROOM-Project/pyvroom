"""VROOM input definition."""

from __future__ import annotations
from typing import Dict, Optional, Sequence, Set, Union
from pathlib import Path

from numpy.typing import ArrayLike
import numpy

from .. import _vroom

from ..amount import Amount
from ..solution.solution import Solution
from ..job import Job, Shipment, ShipmentStep
from ..vehicle import Vehicle


class Input(_vroom.Input):
    """VROOM input defintion.

    Main instance for adding jobs, shipments, vehicles, and cost and duration
    matrice defining a routing problem. Duration matrices is if not provided
    can also be retrieved from a map server.

    Attributes:
        jobs:
            Jobs that needs to be completed in the routing problem.
        vehicles:
            Vehicles available to solve the routing problem.

    """

    _geometry: bool = False
    _distances: bool = False

    def __init__(
        self,
        amount_size: Optional[int] = None,
        servers: Optional[Dict[str, Union[str, _vroom.Server]]] = None,
        router: _vroom.ROUTER = _vroom.ROUTER.OSRM,
    ) -> None:
        """Class initializer.

        Args:
            amount_size:
                The size of the job to be transported. Used to verify all jobs
                have the same size limit.
            servers:
                Assuming no custom duration matrix is provided (from
                `set_durations_matrix`), use this dict to configure the
                routing servers. The key is the routing profile (e.g. "car"),
                the value is host and port in the format `{host}:{port}`.
            router:
                If servers is used, define what kind of server is provided.
                See `vroom.ROUTER` enum for options.
        """
        if servers is None:
            servers = {}
        for key, server in servers.items():
            if isinstance(server, str):
                servers[key] = _vroom.Server(*server.split(":"))
        self._amount_size = amount_size
        self._servers = servers
        self._router = router
        _vroom.Input.__init__(self, servers=servers, router=router)
        if amount_size is not None:
            self._set_amount_size(amount_size)

    def __repr__(self) -> str:
        """String representation."""
        args = []
        if self._amount_size is not None:
            args.append(f"amount_size={self._amount_size}")
        if self._servers:
            args.append(f"servers={self._servers}")
        if self._router != _vroom.ROUTER.OSRM:
            args.append(f"router={self._router}")
        return f"{self.__class__.__name__}({', '.join(args)})"

    @classmethod
    def from_json(
        cls,
        filepath: Path,
        servers: Optional[Dict[str, Union[str, _vroom.Server]]] = None,
        router: _vroom.ROUTER = _vroom.ROUTER.OSRM,
        geometry: Optional[bool] = None,
    ) -> Input:
        """Load model from JSON file.

        Args:
            filepath:
                Path to JSON file with problem definition.
            servers:
                Assuming no custom duration matrix is provided (from
                `set_durations_matrix`), use coordinates and a map server to
                calculate durations matrix. Keys should be identifed by
                `add_routing_wrapper`. If string, values should be on the
                format `{host}:{port}`.
            router:
                If servers is used, define what kind of server is provided.
                See `vroom.ROUTER` enum for options.
            geometry:
                Use coordinates from server instead of from distance matrix.
                If omitted, defaults to `servers is not None`.

        Returns:
            Input instance with all jobs, shipments, etc. added from JSON.

        """
        if geometry is None:
            geometry = servers is not None
        if geometry:
            cls._set_geometry(True)
        instance = Input(servers=servers, router=router)
        with open(filepath) as handle:
            instance._from_json(handle.read(), geometry)
        return instance

    def set_geometry(self):
        self._geometry = True
        return self._set_geometry(True)

    def set_amount_size(self, *amount_sizes: int) -> None:
        """Add amount sizes."""
        sizes = set(amount_sizes)
        if self._amount_size is not None:
            sizes.add(self._amount_size)
        if len(sizes) > 1:
            raise _vroom.VroomInputException(f"Inconsistent capacity lengths: {sizes}")
        if self._amount_size is None:
            size = sizes.pop()
            self._amount_size = size
            self._set_amount_size(size)

    def add_job(
        self,
        job: Union[Job, Shipment, Sequence[Job], Sequence[Shipment]],
    ) -> None:
        """
        Add jobs that needs to be carried out.

        Args:
            job:
                One or more (single) job and/or shipments that the vehicles
                needs to carry out.

        Example:
            >>> problem_instance = vroom.Input()
            >>> problem_instance.add_job(vroom.Job(1, location=1))
            >>> problem_instance.add_job([
            ...     vroom.Job(2, location=2),
            ...     vroom.Shipment(vroom.ShipmentStep(3, location=3),
            ...                    vroom.ShipmentStep(4, location=4)),
            ...     vroom.Job(5, location=5),
            ... ])
        """
        jobs = [job] if isinstance(job, (Job, Shipment)) else job
        for job_ in jobs:
            if isinstance(job_, Job):
                if job_._pickup:
                    self.set_amount_size(len(job_._pickup))
                if job_._delivery:
                    self.set_amount_size(len(job_._delivery))
                self._add_job(job_)

            elif isinstance(job_, Shipment):
                self.set_amount_size(len(job_.amount))
                self._add_shipment(
                    _vroom.Job(
                        id=job_.pickup.id,
                        type=_vroom.JOB_TYPE.PICKUP,
                        location=job_.pickup.location,
                        setup=job_.pickup.setup,
                        service=job_.pickup.service,
                        amount=job_.amount,
                        skills=job_.skills,
                        priority=job_.priority,
                        tws=job_.pickup.time_windows,
                        description=job_.pickup.description,
                    ),
                    _vroom.Job(
                        id=job_.delivery.id,
                        type=_vroom.JOB_TYPE.DELIVERY,
                        location=job_.delivery.location,
                        setup=job_.delivery.setup,
                        service=job_.delivery.service,
                        amount=job_.amount,
                        skills=job_.skills,
                        priority=job_.priority,
                        tws=job_.delivery.time_windows,
                        description=job_.delivery.description,
                    ),
                )

            else:
                raise _vroom.VroomInputException(f"Wrong type for {job_}; vroom.JobSingle expected.")

    def add_shipment(
        self,
        pickup: ShipmentStep,
        delivery: ShipmentStep,
        amount: Amount = Amount(),
        skills: Optional[Set[int]] = None,
        priority: int = 0,
    ):
        """Add a shipment that has to be performed.

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
                The job priority level, where 0 is the most
                important and 100 is the least important.
        """
        self.set_amount_size(len(amount))
        if skills is None:
            skills = set()
        self._add_shipment(
            _vroom.Job(
                id=pickup.id,
                type=_vroom.JOB_TYPE.PICKUP,
                location=pickup.location,
                setup=pickup.setup,
                service=pickup.service,
                amount=amount,
                skills=skills,
                priority=priority,
                tws=pickup.time_windows,
                description=pickup.description,
            ),
            _vroom.Job(
                id=delivery.id,
                type=_vroom.JOB_TYPE.DELIVERY,
                location=delivery.location,
                setup=delivery.setup,
                service=delivery.service,
                amount=amount,
                skills=skills,
                priority=priority,
                tws=delivery.time_windows,
                description=delivery.description,
            ),
        )

    def add_vehicle(
        self,
        vehicle: Union[Vehicle, Sequence[Vehicle]],
    ) -> None:
        """Add vehicle.

        Args:
            vehicle:
                Vehicles to use to solve the vehicle problem. Vehicle type must
                have a recognized profile, and all added vehicle must have the
                same capacity.
        """
        vehicles = [vehicle] if isinstance(vehicle, _vroom.Vehicle) else vehicle
        if not vehicles:
            return
        self.set_amount_size(*[len(vehicle_.capacity) for vehicle_ in vehicles])
        for vehicle_ in vehicles:
            self._add_vehicle(vehicle_)

    def set_durations_matrix(
        self,
        profile: str,
        matrix_input: ArrayLike,
    ) -> None:
        """Set durations matrix.

        Args:
            profile:
                Name of the transportation category profile in question.
                Typically "car", "truck", etc.
            matrix_input:
                A square matrix consisting of duration between each location of
                interest. Diagonal is canonically set to 0.
        """
        assert isinstance(profile, str)
        if not isinstance(matrix_input, _vroom.Matrix):
            matrix_input = _vroom.Matrix(numpy.asarray(matrix_input, dtype="uint32"))
        self._set_durations_matrix(profile, matrix_input)

    def set_distances_matrix(
        self,
        profile: str,
        matrix_input: ArrayLike,
    ) -> None:
        """Set distances matrix.

        Args:
            profile:
                Name of the transportation category profile in question.
                Typically "car", "truck", etc.
            matrix_input:
                A square matrix consisting of distances between each location of
                interest. Diagonal is canonically set to 0.
        """
        assert isinstance(profile, str)
        if not isinstance(matrix_input, _vroom.Matrix):
            matrix_input = _vroom.Matrix(numpy.asarray(matrix_input, dtype="uint32"))
        self._set_distances_matrix(profile, matrix_input)
        self._distances = True

    def set_costs_matrix(
        self,
        profile: str,
        matrix_input: ArrayLike,
    ) -> None:
        """Set costs matrix.

        Args:
            profile:
                Name of the transportation category profile in question.
                Typically "car", "truck", etc.
            matrix_input:
                A square matrix consisting of duration between each location of
                interest. Diagonal is canonically set to 0.
        """
        assert isinstance(profile, str)
        if not isinstance(matrix_input, _vroom.Matrix):
            matrix_input = _vroom.Matrix(numpy.asarray(matrix_input, dtype="uint32"))
        self._set_costs_matrix(profile, matrix_input)

    def solve(
        self,
        exploration_level: int,
        nb_threads: int,
    ) -> Solution:
        solution = Solution(
            self._solve(
                exploration_level=exploration_level,
                nb_threads=nb_threads,
            )
        )
        solution._geometry = self._geometry
        solution._distances = self._distances
        return solution
