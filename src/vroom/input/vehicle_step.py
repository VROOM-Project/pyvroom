from typing import Optional, Sequence, Union

from _vroom import _VehicleStep, JOB_TYPE, STEP_TYPE

from .forced_service import ForcedService


class VehicleStep(_VehicleStep):

    def __init__(
        self,
        *,
        id: Optional[int] = None,
        type: Optional[STEP_TYPE] = None,
        job_type: Optional[JOB_TYPE] = None,
        forced_service: Union[None, Sequence[int], ForcedService] = None,
    ) -> None:
        kwargs = dict(
            id=id,
            type=type,
            job_type=job_type,
            forced_service=forced_service,
        )
        kwargs = {key: value for key, value in kwargs.items()
                  if value is not None}
        self._kwargs = kwargs.copy()
        if isinstance(forced_service, Sequence):
            kwargs["forced_service"] = ForcedService(*forced_service)
        _VehicleStep(**kwargs)

    def __repr__(self) -> str:
        args = [f"{key}={value!r}" for key, value in self._kwargs.items()]
        return f"{self.__class__.__name__}({args})"
