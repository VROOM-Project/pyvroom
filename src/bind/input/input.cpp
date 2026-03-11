#include <fstream>
#include <map>

#include <pybind11/operators.h>
#include <pybind11/chrono.h>

#include "structures/cl_args.cpp"
#include "structures/vroom/input/input.cpp"
#include "utils/input_parser.cpp"

namespace py = pybind11;

void init_input(py::module_ &m) {

  py::class_<vroom::Input>(m, "Input")
      .def(
          py::init([](const vroom::io::Servers &servers, vroom::ROUTER router, bool apply_TSPFix) {
            return new vroom::Input(servers, router, apply_TSPFix);
          }),
          "Class initializer.",
          py::arg("servers") = std::map<std::string, vroom::io::Servers>(),
          py::arg("router") = vroom::ROUTER::OSRM,
          py::arg("apply_TSPFix") = false)
      .def_readonly("jobs", &vroom::Input::jobs)
      .def_readonly("vehicles", &vroom::Input::vehicles)
      .def_readonly("job_id_to_rank", &vroom::Input::job_id_to_rank)
      .def_readonly("pickup_id_to_rank", &vroom::Input::pickup_id_to_rank)
      .def_readonly("delivery_id_to_rank", &vroom::Input::delivery_id_to_rank)
      .def_readonly("compatible_vehicles_for_job", &vroom::Input::compatible_vehicles_for_job)
      .def("_from_json", &vroom::io::parse, py::arg("json_string"),
           py::arg("geometry"))
      .def("_set_geometry", &vroom::Input::set_geometry)
      .def("_add_job", &vroom::Input::add_job)
      .def("_add_shipment", &vroom::Input::add_shipment)
      .def("_add_vehicle", &vroom::Input::add_vehicle)
      .def("_set_durations_matrix",
           [](vroom::Input &self, const std::string &profile,
              vroom::Matrix<vroom::UserDuration> &m) {
             self.set_durations_matrix(profile, std::move(m));
           })
      .def("_set_distances_matrix",
           [](vroom::Input &self, const std::string &profile,
              vroom::Matrix<vroom::UserDistance> &m) {
             self.set_distances_matrix(profile, std::move(m));
           })
      .def("_set_costs_matrix",
           [](vroom::Input &self, const std::string &profile,
              vroom::Matrix<vroom::UserCost> &m) {
             self.set_costs_matrix(profile, std::move(m));
           })
      .def("zero_amount", &vroom::Input::zero_amount)
      .def("apply_TSPFix", &vroom::Input::apply_TSPFix)
      .def("is_used_several_times", &vroom::Input::is_used_several_times)
      .def("has_skills", &vroom::Input::has_skills)
      .def("has_jobs", &vroom::Input::has_jobs)
      .def("has_shipments", &vroom::Input::has_shipments)
      .def("report_distances", &vroom::Input::report_distances)
      .def("get_cost_upper_bound", &vroom::Input::get_cost_upper_bound)
      .def("all_locations_have_coords", &vroom::Input::all_locations_have_coords)
      .def("jobs_vehicles_evals", &vroom::Input::jobs_vehicles_evals)
      .def("has_homogeneous_locations",
           &vroom::Input::has_homogeneous_locations)
      .def("has_homogeneous_profiles", &vroom::Input::has_homogeneous_profiles)
      .def("has_homogeneous_costs", &vroom::Input::has_homogeneous_costs)
      .def("has_initial_routes", &vroom::Input::has_initial_routes)
      .def("vehicle_ok_with_job", &vroom::Input::has_initial_routes)
      .def("vehicle_ok_with_vehicle", &vroom::Input::has_initial_routes)
      .def("_solve",
          [](vroom::Input &self, unsigned exploration_level, unsigned nb_threads, const vroom::Timeout& timeout) {
            return self.solve(exploration_level, nb_threads, timeout);
          },
          "Solve routing problem",
          py::arg("exploration_level"), py::arg("nb_threads"), py::arg("timeout")
          )
      .def("_solve",
          [](vroom::Input &self, unsigned nb_searches, unsigned depth, unsigned nb_threads, const vroom::Timeout& timeout) {
            return self.solve(nb_searches, depth, nb_threads, timeout);
          },
          "Solve routing problem",
          py::arg("nb_searches"), py::arg("depth"), py::arg("nb_threads"), py::arg("timeout")
          )
      .def("check", &vroom::Input::check, "Check solution feasibility", py::arg("nb_thread") = 1);
}
