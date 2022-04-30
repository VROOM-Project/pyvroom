#include "bind/_main.cpp"

#include "bind/amount.cpp"
#include "bind/break.cpp"
#include "bind/enums.cpp"
#include "bind/exception.cpp"
#include "bind/job.cpp"
#include "bind/location.cpp"
#include "bind/time_window.cpp"
#include "bind/vehicle.cpp"

#include "bind/input/input.cpp"
#include "bind/input/vehicle_step.cpp"

#include "bind/generic/matrix.cpp"

#include "bind/solution/route.cpp"
#include "bind/solution/solution.cpp"
#include "bind/solution/step.cpp"
#include "bind/solution/summary.cpp"

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
#include "structures/generic/undirected_graph.cpp"

#include "structures/vroom/cost_wrapper.cpp"
#include "structures/vroom/raw_route.cpp"
#include "structures/vroom/solution_state.cpp"
#include "structures/vroom/tw_route.cpp"

#include "structures/vroom/solution/computing_times.cpp"
#include "structures/vroom/solution/violations.cpp"

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

#include "utils/helpers.h"
#include "utils/version.cpp"

namespace py = pybind11;

PYBIND11_MODULE(_vroom, m) {

  init_enums(m);
  init_exception(m);

  init_matrix(m);

  init_amount(m);
  init_location(m);
  init_time_window(m);
  init_job(m);
  init_vehicle_step(m);
  init_break(m);
  init_vehicle(m);

  init_input(m);

  init_route(m);
  init_solution(m);
  init_step(m);
  init_summary(m);

  init_main(m);

  py::class_<vroom::ComputingTimes>(m, "ComputingTimes").def(py::init<>());

  py::class_<vroom::CostWrapper>(m, "CostWrapper")
      .def(py::init<double>())
      .def("set_durations_matrix", &vroom::CostWrapper::set_durations_matrix)
      .def("set_costs_factor", &vroom::CostWrapper::set_costs_factor)
      .def("set_costs_matrix", &vroom::CostWrapper::set_costs_matrix);

  py::class_<vroom::HeuristicParameters>(m, "HeuristicParameters")
      .def(py::init<vroom::HEURISTIC, vroom::INIT, float>());

  py::class_<vroom::Server>(m, "Server")
      .def(py::init<std::string &, std::string &>(),
           py::arg("host") = "0.0.0.0", py::arg("port") = "5000");

  py::class_<vroom::Violations>(m, "Violations")
      .def(py::init<>())
      .def(py::init([](const vroom::Duration lead_time,
                       const vroom::Duration delay,
                       const std::unordered_set<vroom::VIOLATION> types) {
        return new vroom::Violations(lead_time, delay, std::move(types));
      }))
      .def(py::self += py::self)
      .def_readwrite("_lead_time", &vroom::Violations::lead_time)
      .def_readwrite("_delay", &vroom::Violations::delay)
      .def_readwrite("_types", &vroom::Violations::types);

  py::class_<vroom::routing::HttpWrapper>(m, "HttpWrapper");
  py::class_<vroom::routing::OrsWrapper>(m, "OrsWrapper");
  py::class_<vroom::routing::OsrmRoutedWrapper>(m, "OsrmRoutedWrapper");
  py::class_<vroom::routing::ValhallaWrapper>(m, "ValhallaWrapper");
}
