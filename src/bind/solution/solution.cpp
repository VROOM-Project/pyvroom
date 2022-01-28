#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <string>

#include "structures/vroom/solution/solution.cpp"

namespace py = pybind11;

struct _Step{
  vroom::Id vehicle_id;
  vroom::Id job_id;
  char task[9];
  vroom::Duration arrival;
  vroom::Duration duration;
  vroom::Duration waiting_time;
  vroom::Duration distance;

  vroom::Index loc_index;
  vroom::Index loc_lon;
  vroom::Index loc_lat;

  char description[40];
};


void init_solution(py::module_ &m){

  PYBIND11_NUMPY_DTYPE(_Step, vehicle_id, job_id, task, arrival, duration,
      waiting_time, distance, loc_index, loc_lon, loc_lat, description);

  py::class_<vroom::Solution>(m, "Solution")
    .def(py::init([](vroom::Solution s){ return s; }))
    .def(py::init<unsigned, std::string>())
    .def(py::init([](unsigned code, unsigned amount_size,
                      std::vector<vroom::Route> &routes,
                      std::vector<vroom::Job> &unassigned) {
      return new vroom::Solution(code, amount_size, std::move(routes),
                                  std::move(unassigned));
    }))
    .def("_routes_numpy", [](vroom::Solution solution){
      size_t idx = 0;
      std::string task;
      unsigned int number_of_steps = 0;
      for (auto &route : solution.routes) number_of_steps += route.steps.size();
      auto arr = py::array_t<_Step>(number_of_steps);
      auto ptr = static_cast<_Step*>(arr.request().ptr);
      for (auto &route : solution.routes){
        for (auto &step : route.steps){

          ptr[idx].vehicle_id = route.vehicle;

          if (step.step_type == vroom::STEP_TYPE::START) task = "start";
          else if (step.step_type == vroom::STEP_TYPE::END) task = "end";
          else if (step.step_type == vroom::STEP_TYPE::BREAK) task = "break";
          else if (step.job_type == vroom::JOB_TYPE::SINGLE) task = "single";
          else if (step.job_type == vroom::JOB_TYPE::PICKUP) task = "pickup";
          else if (step.job_type == vroom::JOB_TYPE::DELIVERY) task = "delivery";
          strncpy(ptr[idx].task, task.c_str(), 9);

          ptr[idx].job_id = step.id;
          ptr[idx].arrival = step.arrival;
          ptr[idx].duration = step.duration;
          ptr[idx].waiting_time = step.waiting_time;

          if (step.location.has_coordinates()) {
            ptr[idx].loc_lon = step.location.lon();
            ptr[idx].loc_lat = step.location.lat();
          }
          ptr[idx].loc_index = step.location.index();

          strncpy(ptr[idx].description, step.description.c_str(), 40);

          idx++;
        }
      }
      return arr;
    })
    .def_readwrite("code", &vroom::Solution::code)
    .def_readwrite("error", &vroom::Solution::error)
    .def_readonly("summary", &vroom::Solution::summary)
    .def_readonly("_routes", &vroom::Solution::routes)
    .def_readonly("unassigned", &vroom::Solution::unassigned);

}
