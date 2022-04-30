#include "utils/exception.cpp"

void init_exception(py::module_ &m) {
  py::register_exception<vroom::InternalException>(m, "VroomInternalException");
  py::register_exception<vroom::InputException>(m, "VroomInputException");
  py::register_exception<vroom::RoutingException>(m, "VroomRoutingException");
}
