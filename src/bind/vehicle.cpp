#include <pybind11/pybind11.h>

#include "structures/vroom/vehicle.cpp"

namespace py = pybind11;

void init_vehicle(py::module_ &m) {

  py::class_<vroom::Vehicle>(m, "Vehicle")
      .def(py::init<vroom::Id, std::optional<vroom::Location> &,
                    std::optional<vroom::Location> &, std::string &,
                    vroom::Amount &, vroom::Skills &, vroom::TimeWindow &,
                    std::vector<vroom::Break> &, std::string &, double, size_t,
                    std::vector<vroom::VehicleStep> &>(),
           "Vehicle constructor.", py::arg("id"), py::arg("start"),
           py::arg("end"), py::arg("profile") = vroom::DEFAULT_PROFILE,
           py::arg("capacity") = vroom::Amount(0),
           py::arg("skills") = vroom::Skills(),
           py::arg("time_window") = vroom::TimeWindow(),
           py::arg("breaks") = std::vector<vroom::Break>(),
           py::arg("description") = "", py::arg("speed_factor") = 1.,
           py::arg("max_tasks") = std::numeric_limits<size_t>::max(),
           py::arg("steps") = std::vector<vroom::VehicleStep>())
      // .def("has_start", &vroom::Vehicle::has_start)
      // .def("has_end", &vroom::Vehicle::has_end)
      .def("_has_same_locations", &vroom::Vehicle::has_same_locations)
      .def("_has_same_profile", &vroom::Vehicle::has_same_profile)
      .def_readonly("_id", &vroom::Vehicle::id)
      .def_readwrite("_start", &vroom::Vehicle::start)
      .def_readwrite("_end", &vroom::Vehicle::end)
      .def_readonly("_profile", &vroom::Vehicle::profile)
      .def_readonly("_capacity", &vroom::Vehicle::capacity)
      .def_readonly("_skills", &vroom::Vehicle::skills)
      .def_readonly("_time_window", &vroom::Vehicle::tw)
      .def_readonly("_breaks", &vroom::Vehicle::breaks)
      .def_readonly("_description", &vroom::Vehicle::description)
      // .def_readwrite("_speed_factor", &vroom::Vehicle::speed_factor)
      .def_readonly("_max_tasks", &vroom::Vehicle::max_tasks)
      .def_readonly("_steps", &vroom::Vehicle::steps);
}
