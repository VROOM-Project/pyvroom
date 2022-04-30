import vroom


JOB1 = vroom.Job(id=0, location=1, delivery=[4], pickup=[5])
JOB2 = vroom.Job(
    id=1,
    location=2,
    setup=3,
    service=4,
    delivery=[5],
    pickup=[6],
    skills={7},
    priority=8,
    time_windows=[(9, 10)],
    description="11",
)
JOB3 = vroom.Job(id=0, location=1)

PICKUP1 = vroom.ShipmentStep(id=0, location=1)
DELIVERY1 = vroom.ShipmentStep(id=0, location=1)
SHIPMENT1 = vroom.Shipment(DELIVERY1, PICKUP1)

PICKUP2 = vroom.ShipmentStep(
    id=1,
    location=2,
    setup=3,
    service=4,
    time_windows=[(9, 10)],
    description="12",
)
DELIVERY2 = vroom.ShipmentStep(
    id=1,
    location=2,
    setup=3,
    service=4,
    time_windows=[(9, 10)],
    description="11",
)
SHIPMENT2 = vroom.Shipment(
    PICKUP2,
    DELIVERY2,
    amount=[6],
    skills={7},
    priority=8,
)


def test_job_repr():
    assert repr(JOB1) == "vroom.Job(0, 1, delivery=[4], pickup=[5])"
    assert repr(JOB2) == "vroom.Job(1, 2, setup=3, service=4, delivery=[5], pickup=[6], time_windows=[(9, 10)], description='11')"
    assert repr(JOB3) == "vroom.Job(0, 1)"

    assert repr(PICKUP1) == "vroom.ShipmentStep(0, 1)"
    assert repr(PICKUP2) == "vroom.ShipmentStep(1, 2, setup=3, service=4, time_windows=[(9, 10)], description='12')"

    assert repr(DELIVERY1) == "vroom.ShipmentStep(0, 1)"
    assert repr(DELIVERY2) == "vroom.ShipmentStep(1, 2, setup=3, service=4, time_windows=[(9, 10)], description='11')"

    assert repr(SHIPMENT1) == "vroom.Shipment(vroom.ShipmentStep(0, 1), vroom.ShipmentStep(0, 1))"
    assert repr(SHIPMENT2) == ("vroom.Shipment("
                               "vroom.ShipmentStep(1, 2, setup=3, service=4, time_windows=[(9, 10)], description='12'), "
                               "vroom.ShipmentStep(1, 2, setup=3, service=4, time_windows=[(9, 10)], description='11'), "
                               "amount=[6], skills={7}, priority=8)")


def test_job_attributes():
    assert JOB2.id == 1
    assert JOB2.location == vroom.Location(2)
    assert JOB2.setup == 3
    assert JOB2.service == 4
    assert not hasattr(JOB2, "amount")
    assert JOB2.delivery == vroom.Amount([5])
    assert JOB2.pickup == vroom.Amount([6])
    assert JOB2.skills == {7}
    assert JOB2.priority == 8
    assert JOB2.time_windows == [vroom.TimeWindow(9, 10)]
    assert JOB2.description == "11"

    assert JOB3.delivery == vroom.Amount([])
    assert JOB3.pickup == vroom.Amount([])

    assert DELIVERY2.id == 1
    assert DELIVERY2.location == vroom.Location(2)
    assert DELIVERY2.setup == 3
    assert DELIVERY2.service == 4
    assert not hasattr(DELIVERY2, "delivery")
    assert not hasattr(DELIVERY2, "pickup")
    assert DELIVERY2.time_windows == [vroom.TimeWindow(9, 10)]
    assert DELIVERY2.description == "11"

    assert PICKUP2.id == 1
    assert PICKUP2.location == vroom.Location(2)
    assert PICKUP2.setup == 3
    assert PICKUP2.service == 4
    assert not hasattr(PICKUP2, "delivery")
    assert not hasattr(PICKUP2, "pickup")
    assert PICKUP2.time_windows == [vroom.TimeWindow(9, 10)]
    assert PICKUP2.description == "12"

    assert SHIPMENT2.amount == vroom.Amount([6])
    assert SHIPMENT2.skills == {7}
    assert SHIPMENT2.priority == 8
