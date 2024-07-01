"""An array of integers describing multidimensional quantities."""

from __future__ import annotations
from typing import Sequence, Union

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

    Examples:
        >>> amount = vroom.Amount([1, 2])
        >>> amount[1] = 3
        >>> amount.append(4)
        >>> print(amount)
        vroom.Amount([1, 3, 4])
    """

    def __init__(
        self,
        amount: Union[Amount, Sequence[int], numpy.ndarray] = (),
    ) -> None:
        """
        Initialize.

        Args:
            amount:
                Sequence of quantities to support for. No restriction if omitted.
        """
        _vroom.Amount.__init__(self, numpy.asarray(amount, dtype="longlong"))

    def append(self, amount: int) -> None:
        """Append value to the end of array."""
        self._push_back(amount)

    def __getitem__(self, key: int) -> int:
        return numpy.asarray(self)[key]

    def __eq__(self, other) -> bool:
        if isinstance(other, _vroom.Amount):
            if len(self) != len(other):
                return False
            return bool(numpy.all(numpy.asarray(self) == numpy.asarray(other)))
        return NotImplemented

    def __add__(self, other: Amount) -> Amount:
        other = Amount(other)
        if len(self) != len(other):
            raise _vroom.VroomInternalException("Adding two Amount of different length")
        return Amount(numpy.asarray(self) + numpy.asarray(other))

    def __sub__(self, other: Amount) -> Amount:
        other = Amount(other)
        if len(self) != len(other):
            raise _vroom.VroomInternalException("Subtracting two Amount of different length")
        return Amount(numpy.asarray(self) - numpy.asarray(other))

    def __le__(self, other: Amount) -> bool:
        other = Amount(other)
        if len(self) != len(other):
            raise _vroom.VroomInternalException("Comparing two Amount of different length")
        return self._le(other)

    def __gt__(self, other: Amount) -> bool:
        return not (self.__le__(other))

    def __repr__(self) -> str:
        return f"vroom.{self.__class__.__name__}" f"({numpy.asarray(self).tolist()})"

    def __lshift__(self, other: Amount) -> bool:
        other = Amount(other)
        if len(self) != len(other):
            raise _vroom.VroomInternalException("Comparing two Amount of different length")
        return self._lshift(other)

    def __rshift__(self, other: Amount) -> bool:
        return Amount(other).__lshift__(self)

    def __setitem__(self, key: int, value: int) -> None:
        numpy.asarray(self)[key] = value
