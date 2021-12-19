"""Reproduce the libvroom_example as tests."""
import _vroom
import numpy


def test_example_with_custom_matrix():
    problem_instance = _vroom.Input()

    matrix_input = _vroom.Matrix(numpy.array(
        [[0, 2104, 197, 1299],
         [2103, 0, 2255, 3152],
         [197, 2256, 0, 1102],
         [1299, 3153, 1102, 0]],
        dtype="uint32"))

    problem_instance.set_durations_matrix("car", matrix_input)

    problem_instance.add_vehicle(
        _vroom.Vehicle(0, _vroom.Location(0), _vroom.Location(index=3)))

    problem_instance.add_job(_vroom.Job(id=1414, location=_vroom.Location(index=1)))
    problem_instance.add_job(_vroom.Job(id=1515, location=_vroom.Location(index=2)))

    solution = problem_instance.solve(5, 4)

    assert solution.summary.cost == 5461
    assert solution.summary.unassigned == 0
    assert solution.unassigned == []

    [route] = solution.routes
    assert route.vehicle == 0
    assert route.cost == 5461
    assert route.duration == 5461
    assert route.service == 0
    assert route.distance == 0

    assert ([step.step_type for step in route.steps] ==
            [_vroom.STEP_TYPE.START, _vroom.STEP_TYPE.JOB,
             _vroom.STEP_TYPE.JOB, _vroom.STEP_TYPE.END])
    assert [step.arrival for step in route.steps] == [0, 2104, 4359, 5461]
    assert [step.duration for step in route.steps] == [0, 2104, 4359, 5461]
    assert [step.service for step in route.steps] == [0, 0, 0, 0]
