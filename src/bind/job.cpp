#include <pybind11/operators.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "structures/vroom/job.cpp"

namespace py = pybind11;

void init_job(py::module_ &m) {

  py::class_<vroom::Job>(m, "Job")
      .def(py::init<vroom::Id, vroom::Location &, vroom::Duration,
                    vroom::Duration, vroom::Amount &, vroom::Amount &,
                    vroom::Skills &, vroom::Priority,
                    std::vector<vroom::TimeWindow> &, std::string &>(),
           "Regular one-stop job.", py::arg("id"), py::arg("location"),
           py::arg("setup") = 0, py::arg("service") = 0,
           py::arg("delivery") = vroom::Amount(0),
           py::arg("pickup") = vroom::Amount(0),
           py::arg("skills") = vroom::Skills(), py::arg("priority") = 0,
           py::arg("tws") =
               std::vector<vroom::TimeWindow>(1, vroom::TimeWindow()),
           py::arg("description") = "")
      .def(py::init<vroom::Id, vroom::JOB_TYPE, vroom::Location &,
                    vroom::Duration, vroom::Duration, vroom::Amount &,
                    vroom::Skills &, vroom::Priority,
                    std::vector<vroom::TimeWindow> &, std::string &>(),
           "Pickup and delivery job.", py::arg("id"), py::arg("type"),
           py::arg("location"), py::arg("setup") = 0, py::arg("service") = 0,
           py::arg("amount") = vroom::Amount(0),
           py::arg("skills") = vroom::Skills(), py::arg("priority") = 0,
           py::arg("tws") =
               std::vector<vroom::TimeWindow>(1, vroom::TimeWindow()),
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
}
