"""VROOM input definition."""
from __future__ import annotations
from typing import Dict, Optional, Sequence, Union
from pathlib import Path

from numpy.typing import ArrayLike
import numpy

from .. import _vroom

from ..solution.solution import Solution
from ..job import Job, JobDelivery, JobSingle, JobPickup
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
                `set_durations_matrix`), use coordinates and a map server to
                calculate durations matrix. Keys should be identifed by
                `add_routing_wrapper`. If string, values should be on the
                format `{host}:{port}`.
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

    @staticmethod
    def from_json(
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
        instance = Input(servers=servers, router=router)
        with open(filepath) as handle:
            instance._from_json(handle.read(), geometry)
        return instance

    def set_geometry(self):
        return self._set_geometry()

    def set_amount_size(self, *amount_sizes: int) -> None:
        """Add amount sizes."""
        sizes = set(amount_sizes)
        if self._amount_size is not None:
            sizes.add(self._amount_size)
        if len(sizes) > 1:
            raise _vroom.VroomInputException(
                f"Inconsistent capacity lengths: {sorted(sizes)}")
        if self._amount_size is None:
            size = sizes.pop()
            self._amount_size = size
            self._set_amount_size(size)

    def add_job(
        self,
        *job: Job,
    ) -> None:
        """Add job.

        Jobs should either be `JobSingle` or consequitive a `JobPickup`
        followed by a `JobDelivery`.
        """
        if len(job) == 1 and not isinstance(job[0], _vroom.Job):
            job = job[0]
        jobs = list(job)
        while jobs:
            job = jobs.pop(0)
            if not isinstance(job, Job):
                raise _vroom.VroomInputException("Job input assumed.")
            if isinstance(job, JobSingle):
                self._add_job(job)
            elif isinstance(job, JobPickup):
                if not jobs:
                    raise _vroom.VroomInputException(
                        "A JobPickup should always be followed by JobDelivery.")
                self.add_shipment(job, jobs.pop(0))
            else:
                raise _vroom.VroomInputException(
                    "Jobs must either be SingleJob, or JobPickup followed by a JobDelivery.")

    def add_shipment(
        self,
        pickup: JobPickup,
        delivery: JobDelivery,
    ) -> None:
        """Add shipment."""
        if not isinstance(pickup, JobPickup):
            raise _vroom.VroomInputException(
                "Wrong type for pickup; vroom.JobPickup expected.")
        if not isinstance(delivery, JobDelivery):
            raise _vroom.VroomInputException(
                "Wrong type for delivery; vroom.JobDelivery expected.")
        self.set_amount_size(len(pickup._pickup), len(delivery._delivery))
        self._add_shipment(pickup, delivery)

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
        return Solution(self._solve(
            exploration_level=exploration_level,
            nb_threads=nb_threads,
        ))
