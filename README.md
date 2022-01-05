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
import vroom

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

solution = problem_instance.solve(exploration_level=5, nb_threads=4)

print(solution.summary.cost)
# 5461
for step in solution.routes[0].steps:
    print(step.step_type, step.duration)
# STEP_TYPE.START 0
# STEP_TYPE.JOB 2104
# STEP_TYPE.JOB 4359
# STEP_TYPE.END 5461
```
