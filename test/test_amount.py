import vroom
from vroom import _vroom


def test_amount_init():
    amo1 = _vroom.Amount()
    assert len(amo1) == 0
    amo1._push_back(1)
    amo1._push_back(2)
    amo1._push_back(3)
    assert len(amo1) == 3

    amo2 = vroom.Amount([1, 2, 3])

    assert amo1 == amo2
    assert amo1 != vroom.Amount([3, 2, 1])

    assert amo1
    assert amo2
    assert not vroom.Amount()
    assert not vroom.Amount([])

    assert vroom.Amount(vroom.Amount([1, 2])) == vroom.Amount([1, 2])
    assert str(amo2) == "vroom.Amount([1, 2, 3])"


def test_amount_operator():
    amo1 = vroom.Amount([1, 2, 3])
    amo2 = vroom.Amount([2, 2, 3])

    assert amo1 << amo2
    assert not (amo2 << amo1)
    assert amo2 >> amo1
    assert not (amo1 >> amo2)

    assert amo1 <= amo2
    assert not (amo2 <= amo1)
    assert amo2 >= amo1
    assert not (amo1 >= amo2)

    assert amo1+amo2 == vroom.Amount([3, 4, 6])
    assert amo1-amo2 == vroom.Amount([-1, 0, 0])

    amo1 += amo2
    assert amo1 == vroom.Amount([3, 4, 6])
    amo1 -= amo2+amo2
    assert amo1 == vroom.Amount([-1, 0, 0])


def test_amount_indexing():
    amo = vroom.Amount([1, 2, 3])
    assert amo[1] == 2
    amo[1] = 4
    assert amo == vroom.Amount([1, 4, 3])
