from _vroom import _Amount


class Amount(_Amount):

    def __init__(self, size: int = 0) -> None:
        _Amount.__init__(self, size=size)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.size})"

    @property
    def size(self) -> int:
        return self._size()

