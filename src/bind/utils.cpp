#include <pybind11/pybind11.h>

#include "structures/typedefs.h"

void init_utils(py::module_ &m) {

  m.def("scale_from_user_duration", [](vroom::UserDuration d) {
      return vroom::utils::scale_from_user_duration(d);
  }, py::arg("user_duration"));
  m.def("scale_from_user_duration", [](vroom::TypeToUserDurationMap& d) {
      return vroom::utils::scale_from_user_duration(d);
  }, py::arg("duration_per_type"));
  m.def("scale_to_user_duration", &vroom::utils::scale_to_user_duration,
        py::arg("duration"));
  m.def("scale_from_user_cost", &vroom::utils::scale_from_user_cost,
        py::arg("user_cost"));
  m.def("scale_to_user_cost", &vroom::utils::scale_to_user_cost,
        py::arg("cost"));
}
