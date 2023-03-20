#include <pybind11/pybind11.h>

#include "structures/vroom/vehicle.cpp"

namespace py = pybind11;

void init_vehicle(py::module_ &m) {

  py::class_<vroom::VehicleCosts>(m, "VehicleCosts")
    .def(py::init<vroom::UserCost, vroom::UserCost>(),
        "VehicleCost constructor.",
        py::arg("fixed") = 0, py::arg("per_hour") = 3600)
      .def_readonly("_fixed", &vroom::VehicleCosts::fixed)
      .def_readonly("_per_hour", &vroom::VehicleCosts::per_hour);

  py::class_<vroom::CostWrapper>(m, "CostWrapper")
    .def(py::init<double, vroom::Cost>(),
        "CostWrapper constructor",
        py::arg("speed_factor"), py::arg("per_hour"))
    .def("set_durations_matrix", &vroom::CostWrapper::set_durations_matrix)
    .def("set_costs_matrix", &vroom::CostWrapper::set_costs_matrix)
    .def("_get_speed_factor", &vroom::CostWrapper::get_speed_factor)
    .def("_get_per_hour", &vroom::CostWrapper::get_per_hour);

  py::class_<vroom::Vehicle>(m, "Vehicle")
      .def(py::init<vroom::Id, std::optional<vroom::Location> &,
                    std::optional<vroom::Location> &, std::string &,
                    vroom::Amount &, vroom::Skills &, vroom::TimeWindow &,
                    std::vector<vroom::Break> &, std::string &, vroom::VehicleCosts, double, size_t,
                    std::optional<vroom::Duration>,
                    std::vector<vroom::VehicleStep> &>(),
           "Vehicle constructor.", py::arg("id"), py::arg("start"),
           py::arg("end"), py::arg("profile"),
           py::arg("capacity"),
           py::arg("skills"),
           py::arg("time_window"),
           py::arg("breaks"),
           py::arg("description"),
           py::arg("costs"),
           py::arg("speed_factor"),
           py::arg("max_tasks"),
           py::arg("max_travel_time"),
           py::arg("steps"))
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
      .def_readonly("_costs", &vroom::Vehicle::costs)
      .def_readonly("_cost_wrapper", &vroom::Vehicle::cost_wrapper)
      // .def_readwrite("_speed_factor", &vroom::Vehicle::speed_factor)
      .def_readonly("_max_tasks", &vroom::Vehicle::max_tasks)
      .def_readonly("_max_travel_time", &vroom::Vehicle::max_travel_time)
      .def_readonly("_steps", &vroom::Vehicle::steps);
}
