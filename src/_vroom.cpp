#include "cpp/amount.cpp"
#include "cpp/enums.cpp"
#include "cpp/job.cpp"
#include "cpp/location.cpp"
#include "cpp/time_window.cpp"

#include "cpp/input/vehicle_step.cpp"

#include <pybind11/operators.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "algorithms/kruskal.cpp"
#include "algorithms/munkres.cpp"

#include "algorithms/heuristics/heuristics.cpp"
#include "algorithms/local_search/local_search.cpp"
#include "algorithms/local_search/operator.cpp"
#include "algorithms/validation/check.h"

// #include "routing/libosrm_wrapper.cpp"
#include "routing/http_wrapper.cpp"
#include "routing/ors_wrapper.cpp"
#include "routing/osrm_routed_wrapper.cpp"
#include "routing/valhalla_wrapper.cpp"

#include "structures/typedefs.h"

#include "structures/generic/edge.cpp"
#include "structures/generic/matrix.cpp"
#include "structures/generic/undirected_graph.cpp"

#include "structures/vroom/break.cpp"
#include "structures/vroom/cost_wrapper.cpp"
#include "structures/vroom/raw_route.cpp"
#include "structures/vroom/solution_state.cpp"
#include "structures/vroom/tw_route.cpp"
#include "structures/vroom/vehicle.cpp"

#include "structures/vroom/solution/computing_times.cpp"
#include "structures/vroom/solution/route.cpp"
#include "structures/vroom/solution/solution.cpp"
#include "structures/vroom/solution/step.cpp"
#include "structures/vroom/solution/summary.cpp"
#include "structures/vroom/solution/violations.cpp"

#include "structures/vroom/input/input.cpp"

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
#include "problems/vrptw/vrptw.cpp"

#include "problems/tsp/heuristics/christofides.cpp"
#include "problems/tsp/heuristics/local_search.cpp"
#include "problems/tsp/tsp.cpp"

#include "utils/exception.cpp"
#include "utils/helpers.h"
#include "utils/version.cpp"

namespace py = pybind11;

PYBIND11_MODULE(_vroom, m) {

  init_enums(m);
  init_amount(m);
  init_location(m);
  init_time_window(m);
  init_job(m);
  init_vehicle_step(m);

  py::class_<vroom::Break>(m, "Break")
      .def(py::init<vroom::Id, std::vector<vroom::TimeWindow> &,
                    vroom::Duration, std::string &>())
      .def("is_valid_start", &vroom::Break::is_valid_start);

  py::class_<vroom::ComputingTimes>(m, "ComputingTimes").def(py::init<>());

  py::class_<vroom::CostWrapper>(m, "CostWrapper")
      .def(py::init<double>())
      .def("set_durations_matrix", &vroom::CostWrapper::set_durations_matrix)
      .def("set_costs_factor", &vroom::CostWrapper::set_costs_factor)
      .def("set_costs_matrix", &vroom::CostWrapper::set_costs_matrix);

  py::register_exception<vroom::Exception>(m, "VroomException");
  py::class_<vroom::HeuristicParameters>(m, "HeuristicParameters")
      .def(py::init<vroom::HEURISTIC, vroom::INIT, float>());
  py::class_<vroom::Input>(m, "Input")
      .def(py::init([](unsigned amount_size, const vroom::io::Servers &servers,
                       vroom::ROUTER router) {
             return new vroom::Input(amount_size, servers, router);
           }),
           "Class initializer.", py::arg("amount_size") = 0,
           py::arg("servers") = std::map<std::string, vroom::io::Servers>(),
           py::arg("router") = vroom::ROUTER::OSRM)
      .def_readonly("jobs", &vroom::Input::jobs)
      .def_readonly("vehicles", &vroom::Input::vehicles)
      .def("set_geometry", &vroom::Input::set_geometry)
      .def("add_job", &vroom::Input::add_job)
      .def("add_shipment", &vroom::Input::add_shipment)
      .def("add_vehicle", &vroom::Input::add_vehicle)
      .def("set_durations_matrix",
           [](vroom::Input &self, const std::string &profile,
              vroom::Matrix<vroom::Duration> &m) {
             self.set_durations_matrix(profile, std::move(m));
           })
      .def("set_costs_matrix",
           [](vroom::Input &self, const std::string &profile,
              vroom::Matrix<vroom::Cost> &m) {
             self.set_costs_matrix(profile, std::move(m));
           })
      .def("zero_amount", &vroom::Input::zero_amount)
      .def("has_skills", &vroom::Input::has_skills)
      .def("has_jobs", &vroom::Input::has_jobs)
      .def("has_shipments", &vroom::Input::has_shipments)
      .def("get_cost_upper_bound", &vroom::Input::get_cost_upper_bound)
      .def("has_homogeneous_locations",
           &vroom::Input::has_homogeneous_locations)
      .def("has_homogeneous_profiles", &vroom::Input::has_homogeneous_profiles)
      // .def("vehicle_ok_with_job", &vroom::Input::vehicle_ok_with_job)
      .def("solve", &vroom::Input::solve, "Solve problem.",
           py::arg("exploration_level"), py::arg("nb_threads") = 1,
           py::arg("timeout") = vroom::Timeout(),
           py::arg("h_param") = std::vector<vroom::HeuristicParameters>())
      .def("check", &vroom::Input::check);

  py::class_<vroom::Matrix<uint32_t>>(m, "Matrix", py::buffer_protocol())
      .def(py::init<std::size_t>(), py::arg("size") = 0)
      .def(py::init([](vroom::Matrix<uint32_t> &m) { return m; }))
      .def(py::init([](const py::buffer &b) {
        py::buffer_info info = b.request();
        if (info.format != py::format_descriptor<uint32_t>::format() ||
            info.ndim != 2 || info.shape[0] != info.shape[1])
          throw std::runtime_error("Incompatible buffer format!");
        auto v = new vroom::Matrix<uint32_t>(info.shape[0]);
        memcpy(v->get_data(), info.ptr,
               sizeof(uint32_t) * (size_t)(v->size() * v->size()));
        return v;
      }))
      .def_buffer([](vroom::Matrix<uint32_t> &m) -> py::buffer_info {
        return py::buffer_info(m.get_data(), sizeof(uint32_t),
                               py::format_descriptor<uint32_t>::format(), 2,
                               {m.size(), m.size()},
                               {sizeof(uint32_t) * m.size(), m.size()});
      })
      .def("get_sub_matrix", &vroom::Matrix<uint32_t>::get_sub_matrix)
      .def("size", &vroom::Matrix<uint32_t>::size);

  py::class_<vroom::Route>(m, "Route")
      .def(py::init<>())
      .def(py::init([](vroom::Id vehicle, std::vector<vroom::Step> &steps,
                       vroom::Cost cost, vroom::Duration setup,
                       vroom::Duration service, vroom::Duration duration,
                       vroom::Duration waiting_time, vroom::Priority priority,
                       const vroom::Amount &delivery,
                       const vroom::Amount &pickup, const std::string &profile,
                       const std::string &description,
                       const vroom::Violations &violations) {
        return new vroom::Route(vehicle, std::move(steps), cost, setup, service,
                                duration, waiting_time, priority, delivery,
                                pickup, profile, description,
                                std::move(violations));
      }))
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
      .def(py::init<std::string &, std::string &>(),
           py::arg("host") = "0.0.0.0", py::arg("port") = "5000");

  py::class_<vroom::Solution>(m, "Solution")
      .def(py::init<unsigned, std::string>())
      .def(py::init([](unsigned code, unsigned amount_size,
                       std::vector<vroom::Route> &routes,
                       std::vector<vroom::Job> &unassigned) {
        return new vroom::Solution(code, amount_size, std::move(routes),
                                   std::move(unassigned));
      }))
      .def_readwrite("code", &vroom::Solution::code)
      .def_readwrite("error", &vroom::Solution::error)
      .def_readonly("summary", &vroom::Solution::summary)
      .def_readonly("routes", &vroom::Solution::routes)
      .def_readonly("unassigned", &vroom::Solution::unassigned);

  py::class_<vroom::Step>(m, "Step")
      .def(py::init<vroom::STEP_TYPE, vroom::Location, vroom::Amount>())
      .def(py::init<vroom::Job, vroom::Duration, vroom::Amount>())
      .def(py::init<vroom::Break, vroom::Amount>())
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
      .def_readwrite("violations", &vroom::Summary::violations);

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
           py::arg("tw") = vroom::TimeWindow(),
           py::arg("breaks") = std::vector<vroom::Break>(),
           py::arg("description") = "", py::arg("speed_factor") = 1.,
           py::arg("max_tasks") = std::numeric_limits<size_t>::max(),
           py::arg("input_steps") = std::vector<vroom::VehicleStep>())
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

  py::class_<vroom::Violations>(m, "Violations")
      .def(py::init<>())
      .def(py::init([](const vroom::Duration lead_time,
                       const vroom::Duration delay,
                       const std::unordered_set<vroom::VIOLATION> types) {
        return new vroom::Violations(lead_time, delay, std::move(types));
      }))
      .def(py::self += py::self);

  py::class_<vroom::routing::HttpWrapper>(m, "HttpWrapper");
  py::class_<vroom::routing::OrsWrapper>(m, "OrsWrapper");
  py::class_<vroom::routing::OsrmRoutedWrapper>(m, "OsrmRoutedWrapper");
  py::class_<vroom::routing::ValhallaWrapper>(m, "ValhallaWrapper");

  m.def("get_version", &vroom::get_version, py::return_value_policy::copy);
}
