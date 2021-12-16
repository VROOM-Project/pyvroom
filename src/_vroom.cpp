#include <pybind11/pybind11.h>
#include <pybind11/operators.h>
#include <pybind11/stl.h>

// #include "routing/osrm_routed_wrapper.cpp"
// #include "routing/http_wrapper.cpp"
#include "structures/typedefs.h"
#include "structures/vroom/amount.h"
#include "structures/vroom/break.cpp"
#include "structures/vroom/cost_wrapper.cpp"
#include "structures/vroom/job.cpp"
#include "structures/vroom/location.cpp"
#include "structures/vroom/time_window.cpp"
#include "structures/vroom/vehicle.cpp"

#include "structures/vroom/solution/computing_times.cpp"
#include "structures/vroom/solution/route.cpp"
#include "structures/vroom/solution/violations.cpp"
#include "structures/vroom/solution/solution.cpp"
#include "structures/vroom/solution/step.cpp"
#include "structures/vroom/solution/summary.cpp"

// #include "structures/vroom/input/input.cpp"
#include "structures/vroom/input/vehicle_step.cpp"

#include "utils/exception.cpp"
#include "utils/version.cpp"


namespace py = pybind11;

PYBIND11_MODULE(_vroom, m) {

  // Enumerations
  py::enum_<vroom::ROUTER>(m, "ROUTER")
    .value("OSRM", vroom::ROUTER::OSRM)
    .value("LIBOSRM", vroom::ROUTER::LIBOSRM)
    .value("ORS", vroom::ROUTER::ORS)
    .value("VALHALLA", vroom::ROUTER::VALHALLA)
    .export_values();
  py::enum_<vroom::ERROR>(m, "ERROR")
    .value("INTERNAL", vroom::ERROR::INTERNAL)
    .value("INPUT", vroom::ERROR::INPUT)
    .value("ROUTING", vroom::ERROR::ROUTING)
    .export_values();
  py::enum_<vroom::JOB_TYPE>(m, "JOB_TYPE")
    .value("SINGLE", vroom::JOB_TYPE::SINGLE)
    .value("PICKUP", vroom::JOB_TYPE::PICKUP)
    .value("DELIVERY", vroom::JOB_TYPE::DELIVERY)
    .export_values();
  py::enum_<vroom::STEP_TYPE>(m, "STEP_TYPE")
    .value("START", vroom::STEP_TYPE::START)
    .value("JOB", vroom::STEP_TYPE::JOB)
    .value("BREAK", vroom::STEP_TYPE::BREAK)
    .value("END", vroom::STEP_TYPE::END)
    .export_values();
  py::enum_<vroom::HEURISTIC>(m, "HEURISTIC")
    .value("BASIC", vroom::HEURISTIC::BASIC)
    .value("DYNAMIC", vroom::HEURISTIC::DYNAMIC)
    .value("INIT_ROUTES", vroom::HEURISTIC::INIT_ROUTES)
    .export_values();
  py::enum_<vroom::INIT>(m, "INIT")
    .value("NONE", vroom::INIT::NONE)
    .value("HIGHER_AMOUNT", vroom::INIT::HIGHER_AMOUNT)
    .value("NEAREST", vroom::INIT::NEAREST)
    .value("FURTHEST", vroom::INIT::FURTHEST)
    .value("EARLIEST_DEADLINE", vroom::INIT::EARLIEST_DEADLINE)
    .export_values();
  py::enum_<vroom::VIOLATION>(m, "VIOLATION")
    .value("LEAD_TIME", vroom::VIOLATION::LEAD_TIME)
    .value("DELAY", vroom::VIOLATION::DELAY)
    .value("LOAD", vroom::VIOLATION::LOAD)
    .value("MAX_TASKS", vroom::VIOLATION::MAX_TASKS)
    .value("SKILLS", vroom::VIOLATION::SKILLS)
    .value("PRECEDENCE", vroom::VIOLATION::PRECEDENCE)
    .value("MISSING_BREAK", vroom::VIOLATION::MISSING_BREAK)
    .export_values();

  py::class_<vroom::Amount>(m, "Amount", "The amount in the viechle.")
    .def(py::init([](std::size_t size) { return new vroom::Amount(size); }),
        "Class initializer.", py::arg("size") = 0)
    .def("copy", [](vroom::Amount amount) { return new vroom::Amount(amount); }, "Make a copy of the class")
    .def(py::self += py::self)
    .def(py::self -= py::self)
    .def(py::self == py::self)
    .def("__lshift__", [](const vroom::Amount &a, const vroom::Amount &b){ return a << b; })
    .def("__getitem__", [](const vroom::Amount &a, std::size_t i){ return a[i]; })
    .def("__setitem__", [](vroom::Amount &a, const std::size_t i, const int64_t v){ a[i] = v; })
    .def("empty", &vroom::Amount::empty)
    .def("push_back", &vroom::Amount::push_back)
    .def("size", &vroom::Amount::size);

  py::class_<vroom::Break>(m, "Break")
    .def(py::init<vroom::Id,
                  std::vector<vroom::TimeWindow>&,
                  vroom::Duration,
                  std::string&>())
    .def("is_valid_start", &vroom::Break::is_valid_start);

  py::class_<vroom::ComputingTimes>(m, "ComputingTimes")
    .def(py::init<>());

  py::class_<vroom::CostWrapper>(m, "CostWrapper")
    .def(py::init<double>())
    .def("set_durations_matrix", &vroom::CostWrapper::set_durations_matrix)
    .def("set_costs_factor", &vroom::CostWrapper::set_costs_factor)
    .def("set_costs_matrix", &vroom::CostWrapper::set_costs_matrix);

  py::register_exception<vroom::Exception>(m, "VroomException");

  py::class_<vroom::Job>(m, "Job")
    .def(py::init<vroom::Id,
                  vroom::Location&,
                  vroom::Duration,
                  vroom::Duration,
                  vroom::Amount&,
                  vroom::Amount&,
                  vroom::Skills&,
                  vroom::Priority,
                  std::vector<vroom::TimeWindow>&,
                  std::string&>())
    .def(py::init<vroom::Id,
                  vroom::JOB_TYPE,
                  vroom::Location&,
                  vroom::Duration,
                  vroom::Duration,
                  vroom::Amount&,
                  vroom::Skills&,
                  vroom::Priority,
                  std::vector<vroom::TimeWindow>&,
                  std::string&>())
    .def("index", &vroom::Job::index)
    .def("is_valid_start", &vroom::Job::is_valid_start);

  py::class_<vroom::Location>(m, "Location")
    .def(py::init([](vroom::Index index, const vroom::Coordinates &coords){ return new vroom::Location(index, coords); }))
    .def(py::self == py::self)
    .def("set_index", &vroom::Location::set_index)
    .def("has_coordinates", &vroom::Location::has_coordinates)
    .def("index", &vroom::Location::index)
    .def("lon", &vroom::Location::lon)
    .def("lat", &vroom::Location::lat)
    .def("user_index", &vroom::Location::user_index);

  py::class_<vroom::TimeWindow>(m, "TimeWindow")
    .def(py::init([](vroom::Duration start, vroom::Duration end){
          return new vroom::TimeWindow(start, end); }),
        "Class initializer.",
        py::arg("start") = 0,
        py::arg("end") = vroom::TimeWindow::default_length)
    .def("contains", &vroom::TimeWindow::contains)
    .def("is_default", &vroom::TimeWindow::is_default)
    .def(py::self < py::self);

  py::class_<vroom::Route>(m, "Route")
    .def(py::init<>())
    .def(py::init([](vroom::Id vehicle,
                     std::vector<vroom::Step> &steps,
                     vroom::Cost cost,
                     vroom::Duration setup,
                     vroom::Duration service,
                     vroom::Duration duration,
                     vroom::Duration waiting_time,
                     vroom::Priority priority,
                     const vroom::Amount &delivery,
                     const vroom::Amount &pickup,
                     const std::string &profile,
                     const std::string &description,
                     const vroom::Violations &violations){
          return new vroom::Route(vehicle, std::move(steps), cost, setup, service, duration, waiting_time, priority, delivery, pickup, profile, description, std::move(violations)); }));

  py::class_<vroom::Server>(m, "Server")
    .def(py::init<std::string&, std::string&>(),
         py::arg("host")="0.0.0.0", py::arg("port")="5000");

  py::class_<vroom::Solution>(m, "Solution")
    .def(py::init<unsigned, std::string>())
    .def(py::init([](unsigned code,
                     unsigned amount_size,
                     std::vector<vroom::Route> &routes,
                     std::vector<vroom::Job> &unassigned){return new vroom::Solution(code, amount_size, std::move(routes), std::move(unassigned)); }));


  py::class_<vroom::Step>(m, "Step")
    .def(py::init<vroom::STEP_TYPE,
                  vroom::Location,
                  vroom::Amount>())
    .def(py::init<vroom::Job,
                  vroom::Duration,
                  vroom::Amount>())
    .def(py::init<vroom::Break,
                  vroom::Amount>());

  py::class_<vroom::Summary>(m, "Summary")
    .def(py::init<>())
    .def(py::init<unsigned, unsigned, unsigned>());

  py::class_<vroom::Vehicle>(m, "Vehicle")
    .def(py::init<vroom::Id,
                  std::optional<vroom::Location>&,
                  std::optional<vroom::Location>&,
                  std::string&,
                  vroom::Amount&,
                  vroom::Skills&,
                  vroom::TimeWindow&,
                  std::vector<vroom::Break>&,
                  std::string&,
                  double,
                  size_t,
                  std::vector<vroom::VehicleStep>&>())
    .def("has_start", &vroom::Vehicle::has_start)
    .def("has_end", &vroom::Vehicle::has_end)
    .def("has_same_locations", &vroom::Vehicle::has_same_locations)
    .def("has_same_profile", &vroom::Vehicle::has_same_profile);

  py::class_<vroom::VehicleStep>(m, "VehicleStep")
    .def(py::init([](vroom::STEP_TYPE type, vroom::ForcedService &forced_service){
      return new vroom::VehicleStep(type, std::move(forced_service)); }))
    .def(py::init([](vroom::STEP_TYPE type, vroom::Id id, vroom::ForcedService &forced_service){
      return new vroom::VehicleStep(type, id, std::move(forced_service)); }))
    .def(py::init([](vroom::JOB_TYPE job_type, vroom::Id id, vroom::ForcedService &forced_service){
      return new vroom::VehicleStep(job_type, id, std::move(forced_service)); }));

  py::class_<vroom::Violations>(m, "Violations")
    .def(py::init<>())
    .def(py::init([](const vroom::Duration lead_time,
                     const vroom::Duration delay,
                     const std::unordered_set<vroom::VIOLATION> types){return new vroom::Violations(lead_time, delay, std::move(types)); }))
    .def(py::self += py::self);

  py::class_<vroom::ForcedService>(m, "ForcedService")
    .def(py::init<>())
    .def(py::init<std::optional<vroom::Duration>,
                  std::optional<vroom::Duration>,
                  std::optional<vroom::Duration>>());
  /* py::class_<vroom::Input>(m, "Input"); */

  m.def("get_version", &vroom::get_version, py::return_value_policy::copy);

  // vroom.routing
  /* py::class_<vroom::routing::HttpWrapper>(m, "HttpWrapper"); */
  /*   .def(py::init<std::string&, */
  /*                 vroom::Server&, */
  /*                 std::string&, */
  /*                 std::string&, */
  /*                 std::string&, */
  /*                 std::string&>()) */
  /*   .def("send_then_recieve", &vroom::routing::HttpWrapper::send_then_receive) */
  /*   .def("ssl_send_then_recieve", &vroom::routing::HttpWrapper::ssl_send_then_receive) */
  /*   .def("run_query", &vroom::routing::HttpWrapper::run_query) */
  /*   .def("parse_response", &vroom::routing::HttpWrapper::parse_response) */
  /*   .def("get_matrix", &vroom::routing::HttpWrapper::get_matrix) */
  /*   .def("add_route_info", &vroom::routing::HttpWrapper::add_route_info); */

  /* py::class_<vroom::routing::OsrmRoutedWrapper>(m, "OsrmRoutedWrapper"); */
  /*   .def(py::init<std::string&, vroom::Server&>()); */
}
