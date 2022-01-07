#include "structures/vroom/location.cpp"

#include <pybind11/pybind11.h>

void init_location(py::module_ &m) {

  py::class_<vroom::Location>(m, "Location")
      .def(py::init<vroom::Index>(), py::arg("index"))
      .def(py::init<vroom::Coordinates>(), py::arg("coords"))
      .def(py::init<vroom::Index, vroom::Coordinates>(), py::arg("index"),
           py::arg("coords"))
      .def(py::init([](vroom::Location &l) { return l; }), py::arg("location"))
      .def(py::self == py::self)
      // .def("_set_index", &vroom::Location::set_index)
      .def("_has_coordinates", &vroom::Location::has_coordinates)
      .def("_index", &vroom::Location::index)
      .def("_lon", &vroom::Location::lon)
      .def("_lat", &vroom::Location::lat)
      .def("_user_index", &vroom::Location::user_index);
}
