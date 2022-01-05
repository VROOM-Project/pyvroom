"""An array of integers describing multidimensional quantities."""
from typing import Sequence
import numpy

from . import _vroom  # type: ignore


class Amount(_vroom.Amount):
    """An array of integers describing multidimensional quantities.

    Use amounts  to describe a problem with capacity restrictions. Those arrays
    can be used to model custom restrictions for several metrics at once, e.g.
    number of items, weight, volume etc. A vehicle is only allowed to serve a
    set of tasks if the resulting load at each route step is lower than the
    matching value in capacity for each metric. When using multiple components
    for amounts, it is recommended to put the most important/limiting metrics
    first.

    It is assumed that all delivery-related amounts for jobs are loaded at
    vehicle start, while all pickup-related amounts for jobs are brought back
    at vehicle end.

    Supports the following features:

    * Numpy style indexing.
    * Appending with `.append`.
    * Addition and subtraction when the lengths are equal.
    * Lexicographical compare with `>>` and `<<`.
    * "For all" compare with `<=` and `=<`.
    * "For any" compare with `<` and `>`.

    Args:
        amount:
            Sequence of quantities to support for. No restriction if omitted.

    Examples:
        >>> amount = vroom.Amount([1, 2])
        >>> amount[1] = 3
        >>> amount.append(4)
        >>> print(amount)
        vroom.Amount([1, 3, 4])
    """

    def __init__(
        self,
        amount: Sequence[int] = (),
    ) -> None:
        _vroom.Amount.__init__(self, numpy.asarray(amount, dtype="longlong"))

    def append(self, amount: int) -> None:
        """Append value to the end of array."""
        self._push_back(amount)

    def __getitem__(self, key: int) -> int:
        return numpy.asarray(self)[key]

    def __gt__(self, other) -> bool:
        return not (self.__le__(other))

    def __repr__(self) -> str:
        return f"vroom.{self.__class__.__name__}" f"({numpy.asarray(self).tolist()})"

    def __rshift__(self, other) -> bool:
        return Amount(other).__lshift__(self)

    def __setitem__(self, key: int, value: int) -> None:
        numpy.asarray(self)[key] = value
