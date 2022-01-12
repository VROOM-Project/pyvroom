#include <pybind11/pybind11.h>

#include "structures/vroom/solution/solution.cpp"

namespace py = pybind11;


void init_solution(py::module_ &m){
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
}
