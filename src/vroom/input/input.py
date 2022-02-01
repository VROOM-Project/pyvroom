"""VROOM input definition."""
from __future__ import annotations
from typing import Dict, Optional, Sequence, Union
from pathlib import Path

from numpy.typing import ArrayLike
import numpy

from .. import _vroom

from ..solution.solution import Solution
from ..job import Job
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
        amount_size: int = 0,
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
        if amount_size:
            self._set_amount_size(amount_size)

    def __repr__(self) -> str:
        """String representation."""
        args = []
        if self._amount_size:
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
        geometry = servers is not None
        instance = Input(servers=servers, router=router)
        with open(filepath) as handle:
            instance._from_json(handle.read(), geometry)
        return instance

    def set_geometry(self):
        return self._set_geometry()

    def add_job(
        self,
        job: Union[Job, Sequence[Job]],
    ) -> None:
        if isinstance(job, _vroom.Job):
            job = [job]
        for job_ in job:
            self._add_job(job_)

    def add_shipment(
        self,
        pickup: Job,
        delivery: Job,
    ) -> None:
        self._add_shipment(pickup, delivery)

    def add_vehicle(
        self,
        vehicle: Union[Vehicle, Sequence[Vehicle]],
    ) -> None:
        if isinstance(vehicle, _vroom.Vehicle):
            vehicle = [vehicle]
        for vehicle_ in vehicle:
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
        profile: str,
        matrix_input: ArrayLike,
        self,
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
