Python Vehicle Routing Open-source Optimization Machine
=======================================================

|gh_action| |codecov| |pypi|

.. |gh_action| image:: https://img.shields.io/github/checks-status/VROOM-Project/pyvroom/main
    :target: https://github.com/VROOM-Project/pyvroom/actions
.. |codecov| image:: https://img.shields.io/codecov/c/github/VROOM-Project/pyvroom
    :target: https://codecov.io/gh/VROOM-Project/pyvroom
.. |pypi| image:: https://img.shields.io/pypi/v/pyvroom
    :target: https://pypi.org/project/pyvroom

*Good solution, fast... in Python.*

Pyvroom is an Python wrapper to the excellent `VROOM
<https://github.com/VROOM-Project/vroom>`_ optimization engine for solving
`vehicle routing problems
<https://en.wikipedia.org/wiki/Vehicle_routing_problem>`_.

The library aims to solve several well-known types of vehicle routing problems,
including:

* Travelling salesman.
* Capacitated vehicle routing.
* Routing with time windows.
* Multi-depot heterogeneous vehicle.
* Pickup-and-delivery.

VROOM can also solve any mix of the above problem types.

Basic usage
-----------

.. code:: python

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
  6411

  >>> solution.routes.columns
  Index(['vehicle_id', 'type', 'arrival', 'duration', 'setup', 'service',
         'waiting_time', 'location_index', 'id', 'description'],
        dtype='object')

  >>> solution.routes[["vehicle_id", "type", "arrival", "location_index", "id"]]
     vehicle_id   type  arrival  location_index    id
  0          47  start        0               0  <NA>
  1          47    job     2104               1  1515
  2          47    job     4207               0  1414
  3          47    end     4207               0  <NA>
  4          48  start        0               2  <NA>
  5          48    job     1102               3  1717
  6          48    job     2204               2  1616
  7          48    end     2204               2  <NA>

Usage with a routing engine
---------------------------

.. code:: python

  >>> import vroom

  >>> problem_instance = vroom.Input(
  ...     servers={"auto": "valhalla1.openstreetmap.de:443"},
  ...     router=vroom._vroom.ROUTER.VALHALLA
  ... )

  >>> problem_instance.add_vehicle(vroom.Vehicle(1, start=(2.44, 48.81), profile="auto"))

  >>> problem_instance.add_job([
  ...     vroom.Job(1, location=(2.44, 48.81)),
  ...     vroom.Job(2, location=(2.46, 48.7)),
  ...     vroom.Job(3, location=(2.42, 48.6)),
  ... ])

  >>> sol = problem_instance.solve(exploration_level=5, nb_threads=4)
  >>> print(sol.summary.duration)
  2344

Installation
------------

Pyvroom currently makes binaries for on macOS and Linux. There is also a
Windows build that can be used, but it is somewhat experimental.

Installation of the pre-compiled releases should be as simple as:

.. code:: bash

  pip install pyvroom

Building from source
====================

Building the source distributions requires:

* Download the Pyvroom repository on you local machine:

  .. code:: bash

    git clone --recurse-submodules https://github.com/VROOM-Project/pyvroom

* Install the Python dependencies:

  .. code:: bash

    pip install -r pyvroom/build-requirements.txt

* Install ``asio`` headers, and ``openssl`` and ``crypto`` libraries and headers.
  On Linux and macOS this involve using package managers like ``apt``, ``yum``
  or ``brew``. The exact package name may vary a bit between systems.

* The installation can then be done with:

  .. code:: bash

    pip install pyvroom/

Alternatively it is also possible to install the package from source using
`Conan <https://github.com/conan-io/conan>`_. This is also likely the only
option if installing on Windows.

To install using Conan, do the following:

.. code:: bash

  cd pyvroom/
  conan install --build=openssl --install-folder conan_build .

Documentation
-------------

The code is currently only documented with Pydoc. This means that the best way
to learn Pyvroom for now is to either look at the source code or use ``dir()``
and ``help()`` to navigate the interface.

It is also useful to take a look at the
`VROOM API documentation <https://github.com/VROOM-Project/vroom/blob/master/docs/API.md>`_.
The interface there is mostly the same.
