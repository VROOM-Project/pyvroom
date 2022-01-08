#include "structures/vroom/break.cpp"

#include <pybind11/pybind11.h>

namespace py = pybind11;

void init_break(py::module_ &m) {

  py::class_<vroom::Break>(m, "Break")
      .def(py::init([](vroom::Break &b) { return b; }), py::arg("break"))
      .def(py::init<vroom::Id, std::vector<vroom::TimeWindow> &,
                    vroom::Duration, std::string &>(),
           py::arg("id"), py::arg("time_windows"), py::arg("service"),
           py::arg("description"))
      .def("_is_valid_start", &vroom::Break::is_valid_start, py::arg("time"))
      .def_readwrite("_id", &vroom::Break::id)
      .def_readwrite("_time_windows", &vroom::Break::tws)
      .def_readwrite("_service", &vroom::Break::service)
      .def_readwrite("_description", &vroom::Break::description);
}
