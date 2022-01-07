#include <pybind11/pybind11.h>

#include "structures/vroom/input/vehicle_step.cpp"

namespace py = pybind11;

void init_vehicle_step(py::module_ &m) {

  py::class_<vroom::ForcedService>(m, "ForcedService")
      .def(py::init<>())
      .def(py::init<std::optional<vroom::Duration>,
                    std::optional<vroom::Duration>,
                    std::optional<vroom::Duration>>(),
           py::arg("service_at"), py::arg("service_after"),
           py::arg("service_before"))
      .def_readwrite("_service_at", &vroom::ForcedService::at)
      .def_readwrite("_service_after", &vroom::ForcedService::after)
      .def_readwrite("_service_before", &vroom::ForcedService::before);

  py::class_<vroom::VehicleStep>(m, "VehicleStep")
      .def(py::init([](vroom::VehicleStep v) { return v; }))
      .def(py::init(
               [](vroom::STEP_TYPE type, vroom::ForcedService &forced_service) {
                 return new vroom::VehicleStep(type, std::move(forced_service));
               }),
           py::arg("step_type"), py::arg("forced_service"))
      .def(py::init([](vroom::STEP_TYPE type, vroom::Id id,
                       vroom::ForcedService &forced_service) {
             return new vroom::VehicleStep(type, id, std::move(forced_service));
           }),
           py::arg("step_type"), py::arg("id"), py::arg("forced_service"))
      .def(py::init([](vroom::JOB_TYPE job_type, vroom::Id id,
                       vroom::ForcedService &forced_service) {
             return new vroom::VehicleStep(job_type, id,
                                           std::move(forced_service));
           }),
           py::arg("job_type"), py::arg("id"), py::arg("forced_service"))
      .def_readonly("_step_type", &vroom::VehicleStep::type)
      .def_readonly("_id", &vroom::VehicleStep::id)
      .def_readonly("_type", &vroom::VehicleStep::type)
      .def_readonly("_job_type", &vroom::VehicleStep::job_type)
      .def_readonly("_forced_service", &vroom::VehicleStep::forced_service);
}
