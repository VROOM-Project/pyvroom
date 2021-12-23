"""Reproduce the libvroom_example as tests."""
import vroom


def test_example_with_custom_matrix():
    problem_instance = vroom.Input()

    problem_instance.set_durations_matrix(
        profile="car",
        matrix_input=[[0, 2104, 197, 1299],
                      [2103, 0, 2255, 3152],
                      [197, 2256, 0, 1102],
                      [1299, 3153, 1102, 0]],
    )

    problem_instance.add_vehicle(vroom.Vehicle(0, start=0, end=3))
    problem_instance.add_job(vroom.Job(id=1414, location=1))
    problem_instance.add_job(vroom.Job(id=1515, location=2))

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
            [vroom.STEP_TYPE.START, vroom.STEP_TYPE.JOB,
             vroom.STEP_TYPE.JOB, vroom.STEP_TYPE.END])
    assert [step.arrival for step in route.steps] == [0, 2104, 4359, 5461]
    assert [step.duration for step in route.steps] == [0, 2104, 4359, 5461]
    assert [step.service for step in route.steps] == [0, 0, 0, 0]
