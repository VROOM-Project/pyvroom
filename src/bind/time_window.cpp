#include "structures/vroom/time_window.cpp"

#include <pybind11/pybind11.h>

namespace py = pybind11;

void init_time_window(py::module_ &m) {

  py::class_<vroom::TimeWindow>(m, "TimeWindow")
      .def(py::init([]() { return new vroom::TimeWindow(); }))
      .def(py::init([](vroom::Duration start, vroom::Duration end) {
             return new vroom::TimeWindow(start, end);
           }), py::arg("start"), py::arg("end"))
      .def("_is_default", &vroom::TimeWindow::is_default)
      .def(py::self < py::self)
      .def_readwrite("_start", &vroom::TimeWindow::start)
      .def_readwrite("_end", &vroom::TimeWindow::end)
      .def_readonly_static("_DEFAULT_LENGTH", &vroom::TimeWindow::default_length);
}
