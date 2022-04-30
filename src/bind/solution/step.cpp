#include <pybind11/pybind11.h>

#include "structures/vroom/solution/step.cpp"

namespace py = pybind11;

void init_step(py::module_ &m) {

  py::class_<vroom::Step>(m, "Step")
      .def(py::init<vroom::STEP_TYPE, vroom::Location, vroom::Amount>())
      .def(py::init<vroom::Job, vroom::Duration, vroom::Amount>())
      .def(py::init<vroom::Break, vroom::Amount>())
      .def_readonly("_step_type", &vroom::Step::step_type)
      .def_readonly("_job_type", &vroom::Step::job_type)
      .def_readonly("_location", &vroom::Step::location)
      .def_readonly("_id", &vroom::Step::id)
      .def_readonly("_setup", &vroom::Step::setup)
      .def_readonly("_service", &vroom::Step::service)
      .def_readonly("_load", &vroom::Step::load)
      .def_readonly("_description", &vroom::Step::description)
      .def_readwrite("_arrival", &vroom::Step::arrival)
      .def_readwrite("_duration", &vroom::Step::duration)
      .def_readwrite("_waiting_time", &vroom::Step::waiting_time)
      .def_readwrite("_distance", &vroom::Step::distance)
      .def_readwrite("_violations", &vroom::Step::violations);
}
