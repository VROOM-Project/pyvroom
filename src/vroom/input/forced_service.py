from typing import Optional

from .. import _vroom


class ForcedService(_vroom.ForcedService):
    """
    Force service to abide to cirtain time limits.

    Attributes:
        service_at:
            If not None, the time point the start step should begin at.
        service_after:
            If not None, the time point the start step should begin after.
        service_before:
            If not None, the time point the start step should begin before.

    Examples:
        >>> vroom.ForcedService()
        vroom.ForcedService()
        >>> vroom.ForcedService(
        ...     service_at=1,
        ...     service_after=2,
        ...     service_before=3,
        ... )
        vroom.ForcedService(service_at=1, service_after=2, service_before=3)
    """

    def __init__(
        self,
        *,
        service_at: Optional[int] = None,
        service_after: Optional[int] = None,
        service_before: Optional[int] = None,
    ) -> None:
        """
        Initialize instance.

        Args:
            service_at:
                Constrain start step time to begin at a give time point.
            service_after:
                Constrain start step time to begin after a give time point.
            service_before:
                Constrain start step time to begin before a give time point.
        """
        _vroom.ForcedService.__init__(
            self,
            service_at=service_at,
            service_after=service_after,
            service_before=service_before,
        )

    def __repr__(self) -> str:
        """Create string representation of object."""
        args = []
        if self.service_at is not None:
            args.append(f"service_at={self.service_at}")
        if self.service_after is not None:
            args.append(f"service_after={self.service_after}")
        if self.service_before is not None:
            args.append(f"service_before={self.service_before}")
        return f"vroom.{self.__class__.__name__}({', '.join(args)})"

    @property
    def service_at(self) -> Optional[int]:
        """If not None, the time point the start step should begin at."""
        if self._service_at is None:
            return None
        return _vroom.scale_to_user_duration(self._service_at)

    @property
    def service_after(self) -> Optional[int]:
        """If not None, the time point the start step should begin after."""
        if self._service_after is None:
            return None
        return _vroom.scale_to_user_duration(self._service_after)

    @property
    def service_before(self) -> Optional[int]:
        """If not None, the time point the start step should begin before."""
        if self._service_before is None:
            return None
        return _vroom.scale_to_user_duration(self._service_before)
