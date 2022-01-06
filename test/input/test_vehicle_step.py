import vroom

start1 = vroom.VehicleStep("start")
start2 = vroom.VehicleStepStart()
start3 = vroom.VehicleStepStart(1, 2, 3)

end1 = vroom.VehicleStep("end")
end2 = vroom.VehicleStepEnd()
end3 = vroom.VehicleStepEnd(1, 2, 3)

break1 = vroom.VehicleStep("break", 4)
break2 = vroom.VehicleStepBreak(4)
break3 = vroom.VehicleStepBreak(4, 1, 2, 3)

single1 = vroom.VehicleStep("single", 4)
single2 = vroom.VehicleStepSingle(4)
single3 = vroom.VehicleStepSingle(4, 1, 2, 3)

delivery1 = vroom.VehicleStep("delivery", 4)
delivery2 = vroom.VehicleStepDelivery(4)
delivery3 = vroom.VehicleStepDelivery(4, 1, 2, 3)

pickup1 = vroom.VehicleStep("pickup", 4)
pickup2 = vroom.VehicleStepPickup(4)
pickup3 = vroom.VehicleStepPickup(4, 1, 2, 3)


def test_vehicle_step_subclass():

    assert isinstance(start1, vroom.VehicleStepStart)
    assert not isinstance(start1, vroom.VehicleStepEnd)
    assert not isinstance(start1, vroom.VehicleStepBreak)
    assert not isinstance(start1, vroom.VehicleStepSingle)
    assert not isinstance(start1, vroom.VehicleStepDelivery)
    assert not isinstance(start1, vroom.VehicleStepPickup)

    assert not isinstance(end1, vroom.VehicleStepStart)
    assert isinstance(end1, vroom.VehicleStepEnd)
    assert not isinstance(end1, vroom.VehicleStepBreak)
    assert not isinstance(end1, vroom.VehicleStepSingle)
    assert not isinstance(end1, vroom.VehicleStepDelivery)
    assert not isinstance(end1, vroom.VehicleStepPickup)

    assert not isinstance(break1, vroom.VehicleStepStart)
    assert not isinstance(break1, vroom.VehicleStepEnd)
    assert isinstance(break1, vroom.VehicleStepBreak)
    assert not isinstance(break1, vroom.VehicleStepSingle)
    assert not isinstance(break1, vroom.VehicleStepDelivery)
    assert not isinstance(break1, vroom.VehicleStepPickup)

    assert not isinstance(single1, vroom.VehicleStepStart)
    assert not isinstance(single1, vroom.VehicleStepEnd)
    assert not isinstance(single1, vroom.VehicleStepBreak)
    assert isinstance(single1, vroom.VehicleStepSingle)
    assert not isinstance(single1, vroom.VehicleStepDelivery)
    assert not isinstance(single1, vroom.VehicleStepPickup)

    assert not isinstance(delivery1, vroom.VehicleStepStart)
    assert not isinstance(delivery1, vroom.VehicleStepEnd)
    assert not isinstance(delivery1, vroom.VehicleStepBreak)
    assert not isinstance(delivery1, vroom.VehicleStepSingle)
    assert isinstance(delivery1, vroom.VehicleStepDelivery)
    assert not isinstance(delivery1, vroom.VehicleStepPickup)

    assert not isinstance(pickup1, vroom.VehicleStepStart)
    assert not isinstance(pickup1, vroom.VehicleStepEnd)
    assert not isinstance(pickup1, vroom.VehicleStepBreak)
    assert not isinstance(pickup1, vroom.VehicleStepSingle)
    assert not isinstance(pickup1, vroom.VehicleStepDelivery)
    assert isinstance(pickup1, vroom.VehicleStepPickup)


def test_vehicle_step_init():

    assert isinstance(vroom.VehicleStep(start1), vroom.VehicleStepStart)
    assert isinstance(vroom.VehicleStep(end1), vroom.VehicleStepEnd)
    assert isinstance(vroom.VehicleStep(break1), vroom.VehicleStepBreak)
    assert isinstance(vroom.VehicleStep(single1), vroom.VehicleStepSingle)
    assert isinstance(vroom.VehicleStep(delivery1), vroom.VehicleStepDelivery)
    assert isinstance(vroom.VehicleStep(pickup1), vroom.VehicleStepPickup)

    assert vroom.VehicleStep(start1) == start1
    assert vroom.VehicleStep(end1) == end1
    assert vroom.VehicleStep(break1) == break1
    assert vroom.VehicleStep(single1) == single1
    assert vroom.VehicleStep(delivery1) == delivery1
    assert vroom.VehicleStep(pickup1) == pickup1


def test_vehicle_step_attributes():

    assert start1.id == 0
    assert end2.id == 0
    assert break3.id == 4
    assert single3.service_at == 1
    assert delivery3.service_after == 2
    assert pickup3.service_before == 3
