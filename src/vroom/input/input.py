"""VROOM input definition."""
from numpy.typing import ArrayLike
from typing import Dict, Optional, Union

import numpy

from _vroom import _Input, Matrix, ROUTER, Server


class Input(_Input):
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
        servers: Optional[Dict[str, Union[str, Server]]] = None,
        router: ROUTER = ROUTER.OSRM,
    ) -> None:
        """Class initializer.

        Args:
            amount_size:
                The size of the job to be transported. Used to verify all jobs
                have the same size limit.
            server:
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
                servers[key] = Server(*server.split(":"))
        self._amount_size = amount_size
        self._servers = servers
        self._router = router
        _Input.__init__(
            self,
            amount_size=amount_size,
            servers=servers,
            router=router,
        )

    def __repr__(self) -> str:
        """String representation."""
        args = []
        if self._amount_size:
            args.append(f"amount_size={self._amount_size}")
        if self._servers:
            args.append(f"servers={self._servers}")
        if self._router != ROUTER.OSRM:
            args.append(f"router={self._router}")
        return f"{self.__class__.__name__}({', '.join(args)})"

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
        if not isinstance(matrix_input, Matrix):
            matrix_input = Matrix(numpy.asarray(matrix_input, dtype="uint32"))
        _Input.set_durations_matrix(self, profile, matrix_input)
