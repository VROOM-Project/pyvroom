#include <pybind11/pybind11.h>
#include <pybind11/operators.h>
#include <pybind11/stl.h>

#include "algorithms/kruskal.cpp"
#include "algorithms/munkres.cpp"

#include "algorithms/heuristics/heuristics.cpp"
#include "algorithms/validation/check.h"
#include "algorithms/local_search/local_search.cpp"
#include "algorithms/local_search/operator.cpp"

// #include "routing/libosrm_wrapper.cpp"
#include "routing/http_wrapper.cpp"
#include "routing/ors_wrapper.cpp"
#include "routing/osrm_routed_wrapper.cpp"
#include "routing/valhalla_wrapper.cpp"

#include "structures/typedefs.h"

#include "structures/generic/edge.cpp"
#include "structures/generic/matrix.cpp"
#include "structures/generic/undirected_graph.cpp"

#include "structures/vroom/amount.h"
#include "structures/vroom/break.cpp"
#include "structures/vroom/cost_wrapper.cpp"
#include "structures/vroom/job.cpp"
#include "structures/vroom/location.cpp"
#include "structures/vroom/raw_route.cpp"
#include "structures/vroom/solution_state.cpp"
#include "structures/vroom/time_window.cpp"
#include "structures/vroom/tw_route.cpp"
#include "structures/vroom/vehicle.cpp"

#include "structures/vroom/solution/computing_times.cpp"
#include "structures/vroom/solution/route.cpp"
#include "structures/vroom/solution/violations.cpp"
#include "structures/vroom/solution/solution.cpp"
#include "structures/vroom/solution/step.cpp"
#include "structures/vroom/solution/summary.cpp"

#include "structures/vroom/input/input.cpp"
#include "structures/vroom/input/vehicle_step.cpp"

#include "problems/cvrp/cvrp.cpp"
#include "problems/cvrp/operators/cross_exchange.cpp"
#include "problems/cvrp/operators/intra_cross_exchange.cpp"
#include "problems/cvrp/operators/intra_exchange.cpp"
#include "problems/cvrp/operators/intra_mixed_exchange.cpp"
#include "problems/cvrp/operators/intra_or_opt.cpp"
#include "problems/cvrp/operators/intra_relocate.cpp"
#include "problems/cvrp/operators/mixed_exchange.cpp"
#include "problems/cvrp/operators/or_opt.cpp"
#include "problems/cvrp/operators/pd_shift.cpp"
#include "problems/cvrp/operators/relocate.cpp"
#include "problems/cvrp/operators/reverse_two_opt.cpp"
#include "problems/cvrp/operators/route_exchange.cpp"
#include "problems/cvrp/operators/swap_star.cpp"
#include "problems/cvrp/operators/two_opt.cpp"
#include "problems/cvrp/operators/unassigned_exchange.cpp"
#include "problems/vrp.cpp"

#include "problems/vrptw/vrptw.cpp"
#include "problems/vrptw/operators/cross_exchange.cpp"
#include "problems/vrptw/operators/intra_cross_exchange.cpp"
#include "problems/vrptw/operators/intra_exchange.cpp"
#include "problems/vrptw/operators/intra_mixed_exchange.cpp"
#include "problems/vrptw/operators/intra_or_opt.cpp"
#include "problems/vrptw/operators/intra_relocate.cpp"
#include "problems/vrptw/operators/mixed_exchange.cpp"
#include "problems/vrptw/operators/or_opt.cpp"
#include "problems/vrptw/operators/pd_shift.cpp"
#include "problems/vrptw/operators/relocate.cpp"
#include "problems/vrptw/operators/reverse_two_opt.cpp"
#include "problems/vrptw/operators/route_exchange.cpp"
#include "problems/vrptw/operators/swap_star.cpp"
#include "problems/vrptw/operators/two_opt.cpp"
#include "problems/vrptw/operators/unassigned_exchange.cpp"

#include "problems/tsp/tsp.cpp"
#include "problems/tsp/heuristics/christofides.cpp"
#include "problems/tsp/heuristics/local_search.cpp"

#include "utils/exception.cpp"
#include "utils/helpers.h"
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

  py::class_<vroom::Amount>(m, "Amount", py::buffer_protocol())
    .def(py::init([](std::size_t size) { return new vroom::Amount(size); }),
        py::arg("size") = 0)
    .def(py::init([](vroom::Amount &a){ return a; }), py::arg("amount"))
    .def(py::init([](const py::buffer &b){
            py::buffer_info info = b.request();
            if (info.format != py::format_descriptor<int64_t>::format() || info.ndim != 1)
              throw std::runtime_error("Incompatible buffer format!");
            auto v = new vroom::Amount(info.shape[0]);
            memcpy(v->get_data(), info.ptr,
                   sizeof(int64_t) * (size_t) v->size());
            return v;

        }), py::arg("array"))
    .def_buffer([](vroom::Amount &a) -> py::buffer_info {
        return py::buffer_info(
          a.get_data(),
          sizeof(int64_t),
          py::format_descriptor<int64_t>::format(),
          1,
          {a.size()},
          {sizeof(int64_t)}
        );
    })
    .def(py::self == py::self)
    .def("__add__", [](const vroom::Amount &a, const vroom::Amount &b){
        vroom::Amount c = vroom::Amount(a.size());
        c += a;
        c += b;
        return c;
    })
    .def("__iadd__", [](vroom::Amount &a, const vroom::Amount &b){ a += b; return a; })
    .def("__sub__", [](const vroom::Amount &a, const vroom::Amount &b){
        vroom::Amount c = vroom::Amount(a.size());
        c += a;
        c -= b;
        return c;
    })
    .def("__isub__", [](vroom::Amount &a, const vroom::Amount &b){ a -= b; return a; })
    .def("__lshift__", [](const vroom::Amount &a, const vroom::Amount &b){ return a << b; })
    .def("__le__", [](const vroom::Amount &a, const vroom::Amount &b){ return a <= b; })
    .def("_push_back", &vroom::Amount::push_back)
    .def("__len__", &vroom::Amount::size);

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

  py::class_<vroom::HeuristicParameters>(m, "HeuristicParameters")
    .def(py::init<vroom::HEURISTIC, vroom::INIT, float>());

  py::class_<vroom::Input>(m, "Input")
    .def(
        py::init([](
            unsigned amount_size,
            const vroom::io::Servers &servers,
            vroom::ROUTER router
        ){
          return new vroom::Input(amount_size, servers, router);
        }),
        "Class initializer.",
        py::arg("amount_size") = 0,
        py::arg("servers") = std::map<std::string, vroom::io::Servers>(),
        py::arg("router") = vroom::ROUTER::OSRM
    )
    .def_readonly("jobs", &vroom::Input::jobs)
    .def_readonly("vehicles", &vroom::Input::vehicles)
    .def("set_geometry", &vroom::Input::set_geometry)
    .def("add_job", &vroom::Input::add_job)
    .def("add_shipment", &vroom::Input::add_shipment)
    .def("add_vehicle", &vroom::Input::add_vehicle)
    .def("set_durations_matrix", [](
        vroom::Input &self,
        const std::string &profile,
        vroom::Matrix<vroom::Duration> &m
      ){self.set_durations_matrix(profile, std::move(m)); })
    .def("set_costs_matrix", [](
        vroom::Input &self,
        const std::string &profile,
        vroom::Matrix<vroom::Cost> &m
      ){self.set_costs_matrix(profile, std::move(m)); })
    .def("zero_amount", &vroom::Input::zero_amount)
    .def("has_skills", &vroom::Input::has_skills)
    .def("has_jobs", &vroom::Input::has_jobs)
    .def("has_shipments", &vroom::Input::has_shipments)
    .def("get_cost_upper_bound", &vroom::Input::get_cost_upper_bound)
    .def("has_homogeneous_locations", &vroom::Input::has_homogeneous_locations)
    .def("has_homogeneous_profiles", &vroom::Input::has_homogeneous_profiles)
    // .def("vehicle_ok_with_job", &vroom::Input::vehicle_ok_with_job)
    .def("solve", &vroom::Input::solve, "Solve problem.",
      py::arg("exploration_level"),
      py::arg("nb_threads") = 1,
      py::arg("timeout") = vroom::Timeout(),
      py::arg("h_param") = std::vector<vroom::HeuristicParameters>()
    )
    .def("check", &vroom::Input::check);

  py::class_<vroom::TimeWindow>(m, "TimeWindow")
    .def(py::init([](vroom::Duration start, vroom::Duration end){
          return new vroom::TimeWindow(start, end); }),
        py::arg("start") = 0,
        py::arg("end") = vroom::TimeWindow::default_length)
    .def("_contains", &vroom::TimeWindow::contains)
    // .def("_is_default", &vroom::TimeWindow::is_default)
    .def(py::self < py::self)
    .def_readwrite("start", &vroom::TimeWindow::start)
    .def_readwrite("end", &vroom::TimeWindow::end)
    .def_readonly("_length", &vroom::TimeWindow::length);

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
                  std::string&>(),
        "Regular one-stop job.",
        py::arg("id"),
        py::arg("location"),
        py::arg("setup") = 0,
        py::arg("service") = 0,
        py::arg("delivery") = vroom::Amount(0),
        py::arg("pickup") = vroom::Amount(0),
        py::arg("skills") = vroom::Skills(),
        py::arg("priority") = 0,
        py::arg("tws") = std::vector<vroom::TimeWindow>(1, vroom::TimeWindow()),
        py::arg("description") = "")
    .def(py::init<vroom::Id,
                  vroom::JOB_TYPE,
                  vroom::Location&,
                  vroom::Duration,
                  vroom::Duration,
                  vroom::Amount&,
                  vroom::Skills&,
                  vroom::Priority,
                  std::vector<vroom::TimeWindow>&,
                  std::string&>(),
        "Pickup and delivery job.",
        py::arg("id"),
        py::arg("type"),
        py::arg("location"),
        py::arg("setup") = 0,
        py::arg("service") = 0,
        py::arg("amount") = vroom::Amount(0),
        py::arg("skills") = vroom::Skills(),
        py::arg("priority") = 0,
        py::arg("tws") = std::vector<vroom::TimeWindow>(1, vroom::TimeWindow()),
        py::arg("description") = "")
    .def("index", &vroom::Job::index)
    .def("is_valid_start", &vroom::Job::is_valid_start)
    .def_readonly("_id", &vroom::Job::id)
    .def_readwrite("_location", &vroom::Job::location)
    .def_readonly("_type", &vroom::Job::type)
    .def_readonly("_setup", &vroom::Job::setup)
    .def_readonly("_service", &vroom::Job::service)
    .def_readonly("_delivery", &vroom::Job::delivery)
    .def_readonly("_pickup", &vroom::Job::pickup)
    .def_readonly("_skills", &vroom::Job::skills)
    .def_readonly("_priority", &vroom::Job::priority)
    .def_readonly("_time_windows", &vroom::Job::tws)
    .def_readonly("_description", &vroom::Job::description);

  py::class_<vroom::Location>(m, "Location")
    .def(py::init<vroom::Index>(), py::arg("index"))
    .def(py::init<vroom::Coordinates>(), py::arg("coords"))
    .def(py::init<vroom::Index, vroom::Coordinates>(), py::arg("index"), py::arg("coords"))
    .def(py::init([](vroom::Location &l){return l;}), py::arg("location"))
    .def(py::self == py::self)
    // .def("_set_index", &vroom::Location::set_index)
    .def("_has_coordinates", &vroom::Location::has_coordinates)
    .def("_index", &vroom::Location::index)
    .def("_lon", &vroom::Location::lon)
    .def("_lat", &vroom::Location::lat)
    .def("_user_index", &vroom::Location::user_index);

  py::class_<vroom::Matrix<uint32_t>>(m, "Matrix", py::buffer_protocol())
    .def(py::init<std::size_t>(), py::arg("size") = 0)
    .def(py::init([](vroom::Matrix<uint32_t> &m){ return m; }))
    .def(py::init([](const py::buffer &b){
            py::buffer_info info = b.request();
            if (info.format != py::format_descriptor<uint32_t>::format() || info.ndim != 2 || info.shape[0] != info.shape[1])
              throw std::runtime_error("Incompatible buffer format!");
            auto v = new vroom::Matrix<uint32_t>(info.shape[0]);
            memcpy(v->get_data(), info.ptr,
                   sizeof(uint32_t) * (size_t) (v->size() * v->size()));
            return v;
        }))
    .def_buffer([](vroom::Matrix<uint32_t> &m) -> py::buffer_info {
      return py::buffer_info(
        m.get_data(),
        sizeof(uint32_t),
        py::format_descriptor<uint32_t>::format(),
        2,
        {m.size(), m.size()},
        {sizeof(uint32_t)*m.size(), m.size()}
      );
    })
    .def("get_sub_matrix", &vroom::Matrix<uint32_t>::get_sub_matrix)
    .def("size", &vroom::Matrix<uint32_t>::size);

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
          return new vroom::Route(vehicle, std::move(steps), cost, setup, service, duration, waiting_time, priority, delivery, pickup, profile, description, std::move(violations)); }))
    .def_readwrite("vehicle", &vroom::Route::vehicle)
    .def_readonly("steps", &vroom::Route::steps)
    .def_readwrite("cost", &vroom::Route::cost)
    .def_readwrite("setup", &vroom::Route::setup)
    .def_readwrite("service", &vroom::Route::service)
    .def_readwrite("duration", &vroom::Route::duration)
    .def_readwrite("waiting_time", &vroom::Route::waiting_time)
    .def_readwrite("priority", &vroom::Route::priority)
    .def_readwrite("delivery", &vroom::Route::delivery)
    .def_readwrite("pickup", &vroom::Route::pickup)
    .def_readwrite("profile", &vroom::Route::profile)
    .def_readwrite("description", &vroom::Route::description)
    .def_readwrite("violations", &vroom::Route::violations)
    .def_readwrite("geometry", &vroom::Route::geometry)
    .def_readwrite("distance", &vroom::Route::distance);

  py::class_<vroom::Server>(m, "Server")
    .def(py::init<std::string&, std::string&>(),
         py::arg("host")="0.0.0.0", py::arg("port")="5000");

  py::class_<vroom::Solution>(m, "Solution")
    .def(py::init<unsigned, std::string>())
    .def(py::init([](unsigned code,
                     unsigned amount_size,
                     std::vector<vroom::Route> &routes,
                     std::vector<vroom::Job> &unassigned){return new vroom::Solution(code, amount_size, std::move(routes), std::move(unassigned)); }))
    .def_readwrite("code", &vroom::Solution::code)
    .def_readwrite("error", &vroom::Solution::error)
    .def_readonly("summary", &vroom::Solution::summary)
    .def_readonly("routes", &vroom::Solution::routes)
    .def_readonly("unassigned", &vroom::Solution::unassigned);


  py::class_<vroom::Step>(m, "Step")
    .def(py::init<vroom::STEP_TYPE,
                  vroom::Location,
                  vroom::Amount>())
    .def(py::init<vroom::Job,
                  vroom::Duration,
                  vroom::Amount>())
    .def(py::init<vroom::Break,
                  vroom::Amount>())
    .def_readonly("step_type", &vroom::Step::step_type)
    .def_readonly("job_type", &vroom::Step::job_type)
    .def_readonly("location", &vroom::Step::location)
    .def_readonly("id", &vroom::Step::id)
    .def_readonly("setup", &vroom::Step::setup)
    .def_readonly("service", &vroom::Step::service)
    .def_readonly("load", &vroom::Step::load)
    .def_readonly("description", &vroom::Step::description)
    .def_readwrite("arrival", &vroom::Step::arrival)
    .def_readwrite("duration", &vroom::Step::duration)
    .def_readwrite("waiting_time", &vroom::Step::waiting_time)
    .def_readwrite("distance", &vroom::Step::distance)
    .def_readwrite("violations", &vroom::Step::violations);

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
    .def_readwrite("violations", &vroom::Summary::violations)
    ;

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
                  std::vector<vroom::VehicleStep>&>(),
         "Vehicle constructor.",
         py::arg("id"),
         py::arg("start"),
         py::arg("end"),
         py::arg("profile") = vroom::DEFAULT_PROFILE,
         py::arg("capacity") = vroom::Amount(0),
         py::arg("skills") = vroom::Skills(),
         py::arg("tw") = vroom::TimeWindow(),
         py::arg("breaks") = std::vector<vroom::Break>(),
         py::arg("description") = "",
         py::arg("speed_factor") = 1.,
         py::arg("max_tasks") = std::numeric_limits<size_t>::max(),
         py::arg("input_steps") = std::vector<vroom::VehicleStep>()
    )
    .def("has_start", &vroom::Vehicle::has_start)
    .def("has_end", &vroom::Vehicle::has_end)
    .def("has_same_locations", &vroom::Vehicle::has_same_locations)
    .def("has_same_profile", &vroom::Vehicle::has_same_profile)
    .def_readonly("id", &vroom::Vehicle::id)
    .def_readwrite("_start", &vroom::Vehicle::start)
    .def_readwrite("_end", &vroom::Vehicle::end)
    .def_readonly("profile", &vroom::Vehicle::profile)
    .def_readonly("capacity", &vroom::Vehicle::capacity)
    .def_readonly("skills", &vroom::Vehicle::skills)
    .def_readonly("tw", &vroom::Vehicle::tw)
    .def_readonly("breaks", &vroom::Vehicle::breaks)
    .def_readonly("description", &vroom::Vehicle::description)
    .def_readonly("max_tasks", &vroom::Vehicle::max_tasks)
    .def_readonly("steps", &vroom::Vehicle::steps);

  py::class_<vroom::VehicleStep>(m, "VehicleStep")
    .def(py::init([](vroom::STEP_TYPE type, vroom::ForcedService &forced_service){
      return new vroom::VehicleStep(type, std::move(forced_service)); }))
    .def(py::init([](vroom::STEP_TYPE type, vroom::Id id, vroom::ForcedService &forced_service){
      return new vroom::VehicleStep(type, id, std::move(forced_service)); }))
    .def(py::init([](vroom::JOB_TYPE job_type, vroom::Id id, vroom::ForcedService &forced_service){
      return new vroom::VehicleStep(job_type, id, std::move(forced_service)); }))
    .def_readonly("id", &vroom::VehicleStep::id)
    .def_readonly("type", &vroom::VehicleStep::type)
    .def_readonly("job_type", &vroom::VehicleStep::job_type)
    .def_readonly("forced_service", &vroom::VehicleStep::forced_service);

  py::class_<vroom::Violations>(m, "Violations")
    .def(py::init<>())
    .def(py::init([](const vroom::Duration lead_time,
                     const vroom::Duration delay,
                     const std::unordered_set<vroom::VIOLATION> types){
          return new vroom::Violations(lead_time, delay, std::move(types)); }))
    .def(py::self += py::self);

  py::class_<vroom::ForcedService>(m, "ForcedService")
    .def(py::init<>())
    .def(py::init<std::optional<vroom::Duration>,
                  std::optional<vroom::Duration>,
                  std::optional<vroom::Duration>>())
    .def_readwrite("at", &vroom::ForcedService::at)
    .def_readwrite("after", &vroom::ForcedService::after)
    .def_readwrite("before", &vroom::ForcedService::before);

  py::class_<vroom::routing::HttpWrapper>(m, "HttpWrapper");
  py::class_<vroom::routing::OrsWrapper>(m, "OrsWrapper");
  py::class_<vroom::routing::OsrmRoutedWrapper>(m, "OsrmRoutedWrapper");
  py::class_<vroom::routing::ValhallaWrapper>(m, "ValhallaWrapper");

  m.def("get_version", &vroom::get_version, py::return_value_policy::copy);
}
