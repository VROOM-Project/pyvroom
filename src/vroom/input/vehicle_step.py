from __future__ import annotations

import enum
from typing import Any, Optional, Union

from .. import _vroom


class VEHICLE_STEP_TYPE(str, enum.Enum):
    """The various steps types a vehicle can be in.

    * `start` -- The starting step where the vehicle begins.
    * `end` -- The ending step where the vehicle ends.
    * `break` -- The vehicle is taking a break not performing a task.
    * `single` -- The vehicle is performing a single task.
    * `pickup` -- The vehicle is performing a pickup.
    * `delivery` -- The vehicle is performing a delivery.
    """

    START: str = "start"
    END: str = "end"
    BREAK: str = "break"
    SINGLE: str = "single"
    PICKUP: str = "pickup"
    DELIVERY: str = "delivery"


class VehicleStepBaseclass(_vroom.VehicleStep):
    """Baseclass for VehicleSteps."""

    @property
    def id(self) -> int:
        return self._id

    @property
    def service_at(self) -> Optional[int]:
        if self._forced_service._service_at is None:
            return None
        return _vroom.scale_to_user_duration(self._forced_service._service_at)

    @property
    def service_after(self) -> Optional[int]:
        if self._forced_service._service_after is None:
            return None
        return _vroom.scale_to_user_duration(self._forced_service._service_after)

    @property
    def service_before(self) -> Optional[int]:
        if self._forced_service._service_before is None:
            return None
        return _vroom.scale_to_user_duration(self._forced_service._service_before)

    def __repr__(self) -> str:
        args = []
        if isinstance(
            self,
            (
                VehicleStepBreak,
                VehicleStepSingle,
                VehicleStepPickup,
                VehicleStepDelivery,
            ),
        ):
            args.append(f"{self.id}")
        if self.service_at is not None:
            args.append(f"service_at={self.service_at}")
        if self.service_after is not None:
            args.append(f"service_after={self.service_after}")
        if self.service_before is not None:
            args.append(f"service_before={self.service_before}")
        return f"vroom.{self.__class__.__name__}({', '.join(args)})"

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, _vroom.VehicleStep):
            return (
                self._step_type == other._step_type
                and self._id == other._id
                and (
                    self._forced_service._service_at is other._forced_service._service_at
                    or self._forced_service._service_at == other._forced_service._service_at
                )
                and (
                    self._forced_service._service_after is other._forced_service._service_after
                    or self._forced_service._service_after == other._forced_service._service_after
                )
                and (
                    self._forced_service._service_before is other._forced_service._service_before
                    or self._forced_service._service_before == other._forced_service._service_before
                )
            )
        return NotImplemented


class VehicleStepStart(VehicleStepBaseclass):
    """
    Vehicle step describing the start of the vehicle's journey.

    Attributes:
        service_at:
            If not None, the time point the start step should begin at.
        service_after:
            If not None, the time point the start step should begin after.
        service_before:
            If not None, the time point the start step should begin before.

    Args:
        service_at:
            Constrain start step time to begin at a give time point.
        service_after:
            Constrain start step time to begin after a give time point.
        service_before:
            Constrain start step time to begin before a give time point.

    Examples:
        >>> vroom.VehicleStepStart()
        vroom.VehicleStepStart()

    See also:
        :class:`vroom.VehicleStep`

    """

    def __init__(
        self,
        service_at: Optional[int] = None,
        service_after: Optional[int] = None,
        service_before: Optional[int] = None,
    ) -> None:
        _vroom.VehicleStep.__init__(
            self,
            step_type=_vroom.STEP_TYPE.START,
            forced_service=_vroom.ForcedService(
                service_at=service_at,
                service_after=service_after,
                service_before=service_before,
            ),
        )


class VehicleStepEnd(VehicleStepBaseclass):
    """
    Vehicle step describing the end of the vehicle's journey.

    Attributes:
        service_at:
            If not None, the time point the end step should begin at.
        service_after:
            If not None, the time point the end step should begin after.
        service_before:
            If not None, the time point the end step should begin before.

    Args:
        service_at:
            Constrain end step time to begin at a give time point.
        service_after:
            Constrain end step time to begin after a give time point.
        service_before:
            Constrain end step time to begin before a give time point.

    Examples:
        >>> vroom.VehicleStepEnd()
        vroom.VehicleStepEnd()

    See also:
        :class:`vroom.VehicleStep`

    """

    def __init__(
        self,
        service_at: Optional[int] = None,
        service_after: Optional[int] = None,
        service_before: Optional[int] = None,
    ) -> None:
        _vroom.VehicleStep.__init__(
            self,
            step_type=_vroom.STEP_TYPE.END,
            forced_service=_vroom.ForcedService(
                service_at=service_at,
                service_after=service_after,
                service_before=service_before,
            ),
        )


class VehicleStepBreak(VehicleStepBaseclass):
    """
    Vehicle step describing a break a vehicle must perform.

    Attributes:
        id:
            Reference to the break this step is associated with.
        service_at:
            If not None, the time point the break should begin at.
        service_after:
            If not None, the time point the break should begin after.
        service_before:
            If not None, the time point the break should begin before.

    Args:
        id:
            Reference to the break this step is associated with.
        service_at:
            Constrain break time to begin at a give time point.
        service_after:
            Constrain break time to begin after a give time point.
        service_before:
            Constrain break time to begin before a give time point.

    Examples:
        >>> vroom.VehicleStepBreak(1)
        vroom.VehicleStepBreak(1)

    See also:
        :class:`vroom.VehicleStep`

    """

    def __init__(
        self,
        id: int,
        service_at: Optional[int] = None,
        service_after: Optional[int] = None,
        service_before: Optional[int] = None,
    ) -> None:
        _vroom.VehicleStep.__init__(
            self,
            step_type=_vroom.STEP_TYPE.BREAK,
            id=id,
            forced_service=_vroom.ForcedService(
                service_at=service_at,
                service_after=service_after,
                service_before=service_before,
            ),
        )


class VehicleStepSingle(VehicleStepBaseclass):
    """
    Vehicle step describing a single job a vehicle must perform.

    Attributes:
        id:
            Reference to the single job this step is associated with.
        service_at:
            If not None, the time point the service time should begin at.
        service_after:
            If not None, the time point the service time should begin after.
        service_before:
            If not None, the time point the service time should begin before.

    Args:
        id:
            Reference to the single job this step is associated with.
        service_at:
            Constrain service time to begin at a give time point.
        service_after:
            Constrain service time to begin after a give time point.
        service_before:
            Constrain service time to begin before a give time point.

    Examples:
        >>> vroom.VehicleStepSingle(2)
        vroom.VehicleStepSingle(2)

    See also:
        :class:`vroom.VehicleStep`

    """

    def __init__(
        self,
        id: int,
        service_at: Optional[int] = None,
        service_after: Optional[int] = None,
        service_before: Optional[int] = None,
    ) -> None:
        _vroom.VehicleStep.__init__(
            self,
            job_type=_vroom.JOB_TYPE.SINGLE,
            id=id,
            forced_service=_vroom.ForcedService(
                service_at=service_at,
                service_after=service_after,
                service_before=service_before,
            ),
        )


class VehicleStepDelivery(VehicleStepBaseclass):
    """
    Vehicle step describing a delivery a vehicle must perform.

    Attributes:
        id:
            Reference to the delivery job this step is associated with.
        service_at:
            If not None, the time point the service time should begin at.
        service_after:
            If not None, the time point the service time should begin after.
        service_before:
            If not None, the time point the service time should begin before.

    Args:
        id:
            Reference to the delivery job this step is associated with.
        service_at:
            Constrain service time to begin at a give time point.
        service_after:
            Constrain service time to begin after a give time point.
        service_before:
            Constrain service time to begin before a give time point.

    Examples:
        >>> vroom.VehicleStepDelivery(2)
        vroom.VehicleStepDelivery(2)

    See also:
        :class:`vroom.VehicleStep`

    """

    def __init__(
        self,
        id: int,
        service_at: Optional[int] = None,
        service_after: Optional[int] = None,
        service_before: Optional[int] = None,
    ) -> None:
        _vroom.VehicleStep.__init__(
            self,
            job_type=_vroom.JOB_TYPE.DELIVERY,
            id=id,
            forced_service=_vroom.ForcedService(
                service_at=service_at,
                service_after=service_after,
                service_before=service_before,
            ),
        )


class VehicleStepPickup(VehicleStepBaseclass):
    """
    Vehicle step describing a pickup a vehicle must perform.

    Attributes:
        id:
            Reference to the pickup job this step is associated with.
        service_at:
            If not None, the time point the service time should begin at.
        service_after:
            If not None, the time point the service time should begin after.
        service_before:
            If not None, the time point the service time should begin before.

    Args:
        id:
            Reference to the pickup job this step is associated with.
        service_at:
            Constrain service time to begin at a give time point.
        service_after:
            Constrain service time to begin after a give time point.
        service_before:
            Constrain service time to begin before a give time point.

    Examples:
        >>> vroom.VehicleStepPickup(3)
        vroom.VehicleStepPickup(3)

    See also:
        :class:`vroom.VehicleStep`

    """

    def __init__(
        self,
        id: int,
        service_at: Optional[int] = None,
        service_after: Optional[int] = None,
        service_before: Optional[int] = None,
    ) -> None:
        _vroom.VehicleStep.__init__(
            self,
            job_type=_vroom.JOB_TYPE.PICKUP,
            id=id,
            forced_service=_vroom.ForcedService(
                service_at=service_at,
                service_after=service_after,
                service_before=service_before,
            ),
        )


class VehicleStep(
    VehicleStepStart,
    VehicleStepEnd,
    VehicleStepBreak,
    VehicleStepSingle,
    VehicleStepPickup,
    VehicleStepDelivery,
):
    """
    Vehicle step constructor describing a custom route for a vehicle.

    Depending on `step_type`, creates one of the supported sub-types on
    construction.

    Args:
        step_type:
            The type of step in question. Choose from: `start`, `end`, `break`,
            `single`, `pickup`, and `delivery`.
        id:
            Reference to the job/break the step is associated with.
            Not used for `step_type == "start"` and `step_type == "end"`.
        service_at:
            Hard constraint that the step in question should be performed
            at a give time point.
        service_after:
            Hard constraint that the step in question should be performed
            after a give time point.
        service_before:
            Hard constraint that the step in question should be performed
            before a give time point.

    Examples:
        >>> vroom.VehicleStep("start")
        vroom.VehicleStepStart()
        >>> vroom.VehicleStep("end")
        vroom.VehicleStepEnd()
        >>> vroom.VehicleStep("break", 1)
        vroom.VehicleStepBreak(1)
        >>> vroom.VehicleStep("single", 2)
        vroom.VehicleStepSingle(2)
        >>> vroom.VehicleStep("pickup", 3)
        vroom.VehicleStepPickup(3)
        >>> vroom.VehicleStep("delivery", 4)
        vroom.VehicleStepDelivery(4)

    See also:
        :class:`vroom.VehicleStepStart`
        :class:`vroom.VehicleStepEnd`
        :class:`vroom.VehicleStepBreak`
        :class:`vroom.VehicleStepSingle`
        :class:`vroom.VehicleStepPickup`
        :class:`vroom.VehicleStepDelivery`

    """

    def __new__(
        cls,
        step_type: Union[VehicleStep, VEHICLE_STEP_TYPE],
        id: Optional[int] = None,
        *,
        service_at: Optional[int] = None,
        service_after: Optional[int] = None,
        service_before: Optional[int] = None,
    ):
        """Step that a vehicle is to perform."""
        if isinstance(step_type, _vroom.VehicleStep):
            assert id is None
            assert service_at is None
            assert service_after is None
            assert service_before is None

            id = step_type._id
            if step_type._step_type in (_vroom.STEP_TYPE.START, _vroom.STEP_TYPE.END):
                assert id == 0
                id = None

            service_at = step_type._forced_service._service_at
            service_after = step_type._forced_service._service_after
            service_before = step_type._forced_service._service_before

            if service_at:
                service_at = _vroom.scale_to_user_duration(service_at)
            if service_after:
                service_after = _vroom.scale_to_user_duration(service_after)
            if service_before:
                service_before = _vroom.scale_to_user_duration(service_before)

            if step_type._step_type == _vroom.STEP_TYPE.JOB:
                step_type_map = {
                    _vroom.JOB_TYPE.SINGLE: VEHICLE_STEP_TYPE.SINGLE,
                    _vroom.JOB_TYPE.DELIVERY: VEHICLE_STEP_TYPE.DELIVERY,
                    _vroom.JOB_TYPE.PICKUP: VEHICLE_STEP_TYPE.PICKUP,
                }
                step_type = step_type_map[step_type._job_type]
            else:
                step_type_map = {
                    _vroom.STEP_TYPE.START: VEHICLE_STEP_TYPE.START,
                    _vroom.STEP_TYPE.END: VEHICLE_STEP_TYPE.END,
                    _vroom.STEP_TYPE.BREAK: VEHICLE_STEP_TYPE.BREAK,
                }
                step_type = step_type_map[step_type._step_type]

        kwargs = dict(
            service_at=service_at,
            service_after=service_after,
            service_before=service_before,
        )
        if id is not None:
            kwargs["id"] = id
        step_type = VEHICLE_STEP_TYPE(step_type)
        vehicle_step_classes = {
            VEHICLE_STEP_TYPE.START: VehicleStepStart,
            VEHICLE_STEP_TYPE.END: VehicleStepEnd,
            VEHICLE_STEP_TYPE.BREAK: VehicleStepBreak,
            VEHICLE_STEP_TYPE.SINGLE: VehicleStepSingle,
            VEHICLE_STEP_TYPE.PICKUP: VehicleStepPickup,
            VEHICLE_STEP_TYPE.DELIVERY: VehicleStepDelivery,
        }
        cls = vehicle_step_classes[step_type]

        instance = _vroom.VehicleStep.__new__(cls, **kwargs)
        instance.__init__(**kwargs)
        return instance
