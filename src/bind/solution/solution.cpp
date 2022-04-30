#include <pybind11/iostream.h>
#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>
#include <string>

#include "structures/vroom/solution/solution.cpp"
#include "utils/output_json.cpp"

namespace py = pybind11;

struct _Step {
  int64_t vehicle_id;
  char type[9];
  int64_t arrival;
  int64_t duration;
  int64_t setup;
  int64_t service;
  int64_t waiting_time;
  int64_t distance;
  int64_t longitude;
  int64_t latitude;
  int64_t location_index;
  int64_t id;

  char description[40];
};

void init_solution(py::module_ &m) {

  PYBIND11_NUMPY_DTYPE(_Step, vehicle_id, type, arrival, duration, setup,
                       service, waiting_time, distance, location_index,
                       longitude, latitude, id, description);

  py::class_<vroom::Solution>(m, "Solution")
      .def(py::init([](vroom::Solution s) { return s; }))
      .def(py::init<unsigned, std::string>())
      .def(py::init([](unsigned code, unsigned amount_size,
                       std::vector<vroom::Route> &routes,
                       std::vector<vroom::Job> &unassigned) {
        return new vroom::Solution(code, amount_size, std::move(routes),
                                   std::move(unassigned));
      }))
      .def("_routes_numpy",
           [](vroom::Solution solution) {
             const unsigned int NA_SUBSTITUTE = 4293967297;
             size_t idx = 0;
             std::string type;
             std::string id;
             unsigned int number_of_steps = 0;
             for (auto &route : solution.routes)
               number_of_steps += route.steps.size();
             auto arr = py::array_t<_Step>(number_of_steps);
             auto ptr = static_cast<_Step *>(arr.request().ptr);
             for (auto &route : solution.routes) {
               for (auto &step : route.steps) {

                 ptr[idx].vehicle_id = route.vehicle;

                 if (step.step_type == vroom::STEP_TYPE::START)
                   type = "start";
                 else if (step.step_type == vroom::STEP_TYPE::END)
                   type = "end";
                 else if (step.step_type == vroom::STEP_TYPE::BREAK)
                   type = "break";
                 else if (step.job_type == vroom::JOB_TYPE::SINGLE)
                   type = "job";
                 else if (step.job_type == vroom::JOB_TYPE::PICKUP)
                   type = "pickup";
                 else if (step.job_type == vroom::JOB_TYPE::DELIVERY)
                   type = "delivery";

                 strncpy(ptr[idx].type, type.c_str(), 9);
                 strncpy(ptr[idx].description, step.description.c_str(), 40);

                 ptr[idx].longitude = step.location.has_coordinates()
                                          ? step.location.lon()
                                          : NA_SUBSTITUTE;
                 ptr[idx].latitude = step.location.has_coordinates()
                                         ? step.location.lat()
                                         : NA_SUBSTITUTE;
                 ptr[idx].location_index = step.location.user_index()
                                               ? step.location.index()
                                               : NA_SUBSTITUTE;

                 ptr[idx].id = (step.step_type == vroom::STEP_TYPE::JOB or
                                step.step_type == vroom::STEP_TYPE::BREAK)
                                   ? step.id
                                   : NA_SUBSTITUTE;

                 ptr[idx].setup = step.setup;
                 ptr[idx].service = step.service;
                 ptr[idx].waiting_time = step.waiting_time;
                 ptr[idx].arrival = step.arrival;
                 ptr[idx].duration = step.duration;

                 idx++;
               }
             }
             return arr;
           })
      .def("_solution_json",
           [](vroom::Solution solution) {
             py::scoped_ostream_redirect stream(
                 std::cout, py::module_::import("sys").attr("stdout"));
             vroom::io::write_to_json(solution, false, "");
           })
      .def_readwrite("code", &vroom::Solution::code)
      .def_readwrite("error", &vroom::Solution::error)
      .def_readonly("summary", &vroom::Solution::summary)
      .def_readonly("_routes", &vroom::Solution::routes)
      .def_readonly("unassigned", &vroom::Solution::unassigned);
}
