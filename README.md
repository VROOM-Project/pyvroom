# Python Vehicle Routing Open-source Optimization Machine

_Good solution, fast... in Python._

---

Pyvroom is an Python wrapper to the excellent [VROOM](https://github.com/VROOM-Project/vroom) optimization engine for solving
[vehicle routing problems](https://en.wikipedia.org/wiki/Vehicle_routing_problem).

The library aims to solve several well-known types of vehicle routing problems, including:

- Travelling salesman.
- Capacitated vehicle routing.
- Routing with time windows.
- Multi-depot heterogeneous vehicle.
- Pickup-and-delivery.

VROOM can also solve any mix of the above problem types.

## Installation

Pyvroom currently makes binaries for on MacOS and Linux (Windows is WIP).

Installation should be as simple as:

```bash
pip install pyvroom
```

## Building from source

Building the source distributions on another OS requires:
- the `./build-requirements.txt` Python dependencies
- `asio` headers installed
- `openssl` & `crypto` libraries & headers installed

Optionally the C++ dependencies can be installed with [`conan`](https://github.com/conan-io/conan):
```shell script
conan install --build=openssl --install-folder conan_build .
```
## Basic usage

```python
>>> import vroom

>>> problem_instance = vroom.Input()

>>> problem_instance.set_durations_matrix(
...     profile="car",
...     matrix_input=[[0, 2104, 197, 1299],
...                   [2103, 0, 2255, 3152],
...                   [197, 2256, 0, 1102],
...                   [1299, 3153, 1102, 0]],
... )

>>> problem_instance.add_vehicle([vroom.Vehicle(47, start=0, end=0),
...                               vroom.Vehicle(48, start=2, end=2)])

>>> problem_instance.add_job([vroom.Job(1414, location=0),
...                           vroom.Job(1515, location=1),
...                           vroom.Job(1616, location=2),
...                           vroom.Job(1717, location=3)])

>>> solution = problem_instance.solve(exploration_level=5, nb_threads=4)

>>> solution.summary.cost
3206

>>> solution.routes
   vehicle_id  job_id    task  arrival  loc_index
0          47       0   start        0          0
1          47    1515  single     2104          1
2          47    1414  single     4207          0
3          47       0     end     4207          0
4          48       0   start        0          2
5          48    1717  single     1102          3
6          48    1616  single     2204          2
7          48       0     end     2204          2
```
