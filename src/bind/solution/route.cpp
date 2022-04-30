#include <pybind11/pybind11.h>

#include "structures/vroom/solution/route.cpp"

namespace py = pybind11;

void init_route(py::module_ &m) {

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
}
