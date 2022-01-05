import vroom


JOB_SINGLE1 = vroom.Job(id=0, location=1, delivery=[4], pickup=[5])
JOB_SINGLE2 = vroom.JobSingle(id=0, location=1, delivery=[4], pickup=[5])
JOB_SINGLE3 = vroom.JobSingle(
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
JOB_SINGLE4 = vroom.Job(id=0, location=1)

JOB_DELIVERY1 = vroom.Job(id=0, location=1, delivery=[4])
JOB_DELIVERY2 = vroom.JobDelivery(id=0, location=1, amount=[4])
JOB_DELIVERY3 = vroom.JobDelivery(
    id=1,
    location=2,
    setup=3,
    service=4,
    amount=[5],
    skills={7},
    priority=8,
    time_windows=[(9, 10)],
    description="11",
)

JOB_PICKUP1 = vroom.Job(id=0, location=1, pickup=[4])
JOB_PICKUP2 = vroom.JobPickup(id=0, location=1, amount=[4])
JOB_PICKUP3 = vroom.JobPickup(
    id=1,
    location=2,
    setup=3,
    service=4,
    amount=[6],
    skills={7},
    priority=8,
    time_windows=[(9, 10)],
    description="11",
)


def test_job_repr():
    assert repr(JOB_SINGLE1) == "vroom.JobSingle(0, 1, delivery=[4], pickup=[5])"
    assert repr(JOB_SINGLE3) == ("vroom.JobSingle(1, 2, setup=3, service=4, delivery=[5], pickup=[6], "
                                 "skills={7}, priority=8, time_windows=[(9, 10)], description='11')")
    assert repr(JOB_SINGLE4) == "vroom.JobSingle(0, 1)"
    assert repr(JOB_DELIVERY1) == "vroom.JobDelivery(0, 1, amount=[4])"
    assert repr(JOB_DELIVERY3) == ("vroom.JobDelivery(1, 2, setup=3, service=4, amount=[5], skills={7}, "
                                   "priority=8, time_windows=[(9, 10)], description='11')")
    assert repr(JOB_PICKUP1) == "vroom.JobPickup(0, 1, amount=[4])"
    assert repr(JOB_PICKUP3) == ("vroom.JobPickup(1, 2, setup=3, service=4, amount=[6], skills={7}, "
                                 "priority=8, time_windows=[(9, 10)], description='11')")


def test_job_subclass():
    # assert isinstance(JOB_SINGLE1, vroom.Job)
    assert isinstance(JOB_SINGLE1, vroom.JobSingle)
    assert not isinstance(JOB_SINGLE1, vroom.JobDelivery)
    assert not isinstance(JOB_SINGLE1, vroom.JobPickup)

    # assert isinstance(JOB_SINGLE2, vroom.Job)
    assert isinstance(JOB_SINGLE2, vroom.JobSingle)
    assert not isinstance(JOB_SINGLE2, vroom.JobDelivery)
    assert not isinstance(JOB_SINGLE2, vroom.JobPickup)

    # assert isinstance(JOB_SINGLE4, vroom.Job)
    assert isinstance(JOB_SINGLE4, vroom.JobSingle)
    assert not isinstance(JOB_SINGLE4, vroom.JobDelivery)
    assert not isinstance(JOB_SINGLE4, vroom.JobPickup)

    # assert isinstance(JOB_DELIVERY1, vroom.Job)
    assert not isinstance(JOB_DELIVERY1, vroom.JobSingle)
    assert isinstance(JOB_DELIVERY1, vroom.JobDelivery)
    assert not isinstance(JOB_DELIVERY1, vroom.JobPickup)

    # assert isinstance(JOB_DELIVERY2, vroom.Job)
    assert not isinstance(JOB_DELIVERY2, vroom.JobSingle)
    assert isinstance(JOB_DELIVERY2, vroom.JobDelivery)
    assert not isinstance(JOB_DELIVERY2, vroom.JobPickup)

    # assert isinstance(JOB_PICKUP1, vroom.Job)
    assert not isinstance(JOB_PICKUP1, vroom.JobSingle)
    assert not isinstance(JOB_PICKUP1, vroom.JobDelivery)
    assert isinstance(JOB_PICKUP1, vroom.JobPickup)

    # assert isinstance(JOB_PICKUP2, vroom.Job)
    assert not isinstance(JOB_PICKUP2, vroom.JobSingle)
    assert not isinstance(JOB_PICKUP2, vroom.JobDelivery)
    assert isinstance(JOB_PICKUP2, vroom.JobPickup)


def test_job_attributes():
    assert JOB_SINGLE3.id == 1
    assert JOB_SINGLE3.location == vroom.Location(2)
    assert JOB_SINGLE3.setup == 3
    assert JOB_SINGLE3.service == 4
    assert not hasattr(JOB_SINGLE3, "amount")
    assert JOB_SINGLE3.delivery == vroom.Amount([5])
    assert JOB_SINGLE3.pickup == vroom.Amount([6])
    assert JOB_SINGLE3.skills == {7}
    assert JOB_SINGLE3.priority == 8
    assert JOB_SINGLE3.time_windows == [vroom.TimeWindow(9, 10)]
    assert JOB_SINGLE3.description == "11"

    assert JOB_SINGLE4.delivery == vroom.Amount([])
    assert JOB_SINGLE4.pickup == vroom.Amount([])

    assert JOB_DELIVERY3.id == 1
    assert JOB_DELIVERY3.location == vroom.Location(2)
    assert JOB_DELIVERY3.setup == 3
    assert JOB_DELIVERY3.service == 4
    assert JOB_DELIVERY3.amount == vroom.Amount([5])
    assert not hasattr(JOB_DELIVERY3, "delivery")
    assert not hasattr(JOB_DELIVERY3, "pickup")
    assert JOB_DELIVERY3.skills == {7}
    assert JOB_DELIVERY3.priority == 8
    assert JOB_DELIVERY3.time_windows == [vroom.TimeWindow(9, 10)]
    assert JOB_DELIVERY3.description == "11"

    assert JOB_PICKUP3.id == 1
    assert JOB_PICKUP3.location == vroom.Location(2)
    assert JOB_PICKUP3.setup == 3
    assert JOB_PICKUP3.service == 4
    assert JOB_PICKUP3.amount == vroom.Amount([6])
    assert not hasattr(JOB_PICKUP3, "delivery")
    assert not hasattr(JOB_PICKUP3, "pickup")
    assert JOB_PICKUP3.skills == {7}
    assert JOB_PICKUP3.priority == 8
    assert JOB_PICKUP3.time_windows == [vroom.TimeWindow(9, 10)]
    assert JOB_PICKUP3.description == "11"
