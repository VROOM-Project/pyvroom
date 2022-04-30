#include <pybind11/pybind11.h>

#include "structures/vroom/solution/summary.cpp"

namespace py = pybind11;

void init_summary(py::module_ &m) {

  py::class_<vroom::Summary>(m, "Summary")
      .def(py::init<>())
      .def(py::init<unsigned, unsigned, unsigned>())
      .def_readwrite("cost", &vroom::Summary::cost)
      .def_readonly("routes", &vroom::Summary::routes)
      .def_readonly("unassigned", &vroom::Summary::unassigned)
      .def_readwrite("delivery", &vroom::Summary::delivery)
      .def_readwrite("pickup", &vroom::Summary::pickup)
      .def_readwrite("setup", &vroom::Summary::setup)
      .def_readwrite("service", &vroom::Summary::service)
      .def_readwrite("priority", &vroom::Summary::priority)
      .def_readwrite("duration", &vroom::Summary::duration)
      .def_readwrite("waiting_time", &vroom::Summary::waiting_time)
      .def_readwrite("distance", &vroom::Summary::distance)
      .def_readwrite("computing_times", &vroom::Summary::computing_times)
      .def_readwrite("violations", &vroom::Summary::violations);
}
