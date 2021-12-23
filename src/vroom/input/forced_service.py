
from _vroom import _ForcedService
from typing import Optional

class ForcedService(_ForcedService):
    """
    Examples:
        >>> vroom.ForcedService()
        vroom.ForcedService()
    """

    def __init__(
        self,
        at: Optional[int] = None,
        after: Optional[int] = None,
        before: Optional[int] = None,
    ) -> None:
        kwargs = dict(at=at, after=after, before=before)
        self._kwargs = {key: value for key, value in kwargs.items()
                        if value is not None}
        _ForcedService.__init__(self, **self._kwargs)

    def __repr__(self) -> str:
        args = ", ".join(f"{key}={value}"
                         for key, value in self._kwargs.items())
        return f"vroom.{self.__class__.__name__}({args})"

    @property
    def at(self) -> int:
        return self._kwargs["at"]

    @property
    def after(self) -> int:
        return self._kwargs["after"]

    @property
    def before(self) -> int:
        return self._kwargs["before"]
