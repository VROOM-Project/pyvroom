#include <pybind11/pybind11.h>

#include "structures/typedefs.h"

void init_utils(py::module_ &m) {

  m.def(
      "scale_from_user_duration",
      &vroom::utils::scale_from_user_duration,
      py::arg("duration")
  );
  m.def(
      "scale_to_user_duration",
      &vroom::utils::scale_to_user_duration,
      py::arg("duration")
  );
  m.def(
      "scale_to_user_cost",
      &vroom::utils::scale_to_user_cost,
      py::arg("cost")
  );

}
