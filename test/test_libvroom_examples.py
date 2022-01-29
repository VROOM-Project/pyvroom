"""Reproduce the libvroom_example as tests."""
import numpy
import pandas

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
    problem_instance.add_vehicle([vroom.Vehicle(7, start=0, end=0),
                                  vroom.Vehicle(8, start=2, end=2)])
    problem_instance.add_job([vroom.Job(id=1414, location=0),
                              vroom.Job(id=1515, location=1),
                              vroom.Job(id=1616, location=2),
                              vroom.Job(id=1717, location=3)])
    solution = problem_instance.solve(
        exploration_level=5, nb_threads=4)

    assert solution.summary.cost == 6411
    assert solution.summary.unassigned == 0
    assert solution.unassigned == []

    routes = solution.routes
    assert numpy.all(routes.vehicle_id.drop_duplicates() == [7, 8])
    assert numpy.all(routes.id == [None, 1515, 1414, None,
                                   None, 1717, 1616, None])
    assert numpy.all(routes.type == ["start", "job", "job", "end",
                                     "start", "job", "job", "end"])
    assert numpy.all(routes.arrival == [0, 2104, 4207, 4207,
                                        0, 1102, 2204, 2204])
    assert numpy.all(routes.location_index == [0, 1, 0, 0, 2, 3, 2, 2])
