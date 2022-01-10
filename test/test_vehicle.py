import vroom


def test_repr():

    assert (repr(vroom.Vehicle(1, start=4, profile="bus"))
            == "vroom.Vehicle(1, start=4, profile='bus')")
    assert (repr(vroom.Vehicle(2, end=(2., 3.), capacity=[1, 2]))
            == "vroom.Vehicle(2, end=(2.0, 3.0), capacity=[1, 2])")
    assert (repr(vroom.Vehicle(2, start=vroom.Location(index=2, coords=(4., 5.)), skills={7}))
            == "vroom.Vehicle(2, start=vroom.Location(index=2, coords=(4.0, 5.0)), skills={7})")
    assert (repr(vroom.Vehicle(3, start=7, time_window=(3, 4)))
            == "vroom.Vehicle(3, start=7, time_window=(3, 4))")
    assert (repr(vroom.Vehicle(3, end=7, breaks=[vroom.Break(4, [(1, 2)])]))
            == "vroom.Vehicle(3, end=7, breaks=[vroom.Break(4, time_windows=[(1, 2)])])")
    assert (repr(vroom.Vehicle(3, start=7, description="hello"))
            == "vroom.Vehicle(3, start=7, description='hello')")
    assert (repr(vroom.Vehicle(3, end=7, speed_factor=2.))
            == "vroom.Vehicle(3, end=7, speed_factor=2.0)")
    assert (repr(vroom.Vehicle(3, start=7, max_tasks=17))
            == "vroom.Vehicle(3, start=7, max_tasks=17)")
    assert (repr(vroom.Vehicle(3, end=7, steps=[vroom.VehicleStep("single", 3)]))
            == """vroom.Vehicle(3, end=7, \
steps=[vroom.VehicleStepStart(), vroom.VehicleStepSingle(3), vroom.VehicleStepEnd()])""")
