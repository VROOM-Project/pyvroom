#include "structures/vroom/time_window.cpp"

#include <pybind11/pybind11.h>

namespace py = pybind11;

void init_time_window(py::module_ &m) {

  py::class_<vroom::TimeWindow>(m, "TimeWindow")
      .def(py::init([](vroom::Duration start, vroom::Duration end) {
             return new vroom::TimeWindow(start, end);
           }),
           py::arg("start") = 0,
           py::arg("end") = vroom::TimeWindow::default_length)
      .def("_contains", &vroom::TimeWindow::contains)
      // .def("_is_default", &vroom::TimeWindow::is_default)
      .def(py::self < py::self)
      .def_readwrite("start", &vroom::TimeWindow::start)
      .def_readwrite("end", &vroom::TimeWindow::end)
      .def_readonly("_length", &vroom::TimeWindow::length);
}
