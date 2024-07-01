"""Vehicle routing open-source optimization machine (VROOM)."""

import sys
from typing import Optional, Sequence
from ._vroom import _main, JOB_TYPE, STEP_TYPE  # type: ignore

from .amount import Amount
from .break_ import Break
from .job import Job, ShipmentStep, Shipment
from .location import Location, LocationCoordinates, LocationIndex
from .time_window import TimeWindow
from .vehicle import Vehicle, VehicleCosts

from .input.forced_service import ForcedService
from .input.input import Input
from .input.vehicle_step import (
    VehicleStep,
    VehicleStepStart,
    VehicleStepEnd,
    VehicleStepBreak,
    VehicleStepSingle,
    VehicleStepPickup,
    VehicleStepDelivery,
    VEHICLE_STEP_TYPE,
)


def main(argv: Optional[Sequence[str]] = None) -> None:
    """Run VROOM command line interface."""
    _main(sys.argv if argv is None else argv)
