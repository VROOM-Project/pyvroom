#include <pybind11/pybind11.h>

#include "structures/vroom/solution/step.cpp"

namespace py = pybind11;


void init_step(py::module_ &m){

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
}
