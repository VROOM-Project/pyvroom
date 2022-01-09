#include <pybind11/pybind11.h>

#include "structures/typedefs.h"

namespace py = pybind11;

void init_enums(py::module_ &m) {

  py::enum_<vroom::ROUTER>(m, "ROUTER")
      .value("OSRM", vroom::ROUTER::OSRM)
      .value("LIBOSRM", vroom::ROUTER::LIBOSRM)
      .value("ORS", vroom::ROUTER::ORS)
      .value("VALHALLA", vroom::ROUTER::VALHALLA)
      .export_values();

  py::enum_<vroom::JOB_TYPE>(m, "JOB_TYPE")
      .value("SINGLE", vroom::JOB_TYPE::SINGLE)
      .value("PICKUP", vroom::JOB_TYPE::PICKUP)
      .value("DELIVERY", vroom::JOB_TYPE::DELIVERY)
      .export_values();

  py::enum_<vroom::STEP_TYPE>(m, "STEP_TYPE")
      .value("START", vroom::STEP_TYPE::START)
      .value("JOB", vroom::STEP_TYPE::JOB)
      .value("BREAK", vroom::STEP_TYPE::BREAK)
      .value("END", vroom::STEP_TYPE::END)
      .export_values();

  py::enum_<vroom::HEURISTIC>(m, "HEURISTIC")
      .value("BASIC", vroom::HEURISTIC::BASIC)
      .value("DYNAMIC", vroom::HEURISTIC::DYNAMIC)
      .value("INIT_ROUTES", vroom::HEURISTIC::INIT_ROUTES)
      .export_values();

  py::enum_<vroom::INIT>(m, "INIT")
      .value("NONE", vroom::INIT::NONE)
      .value("HIGHER_AMOUNT", vroom::INIT::HIGHER_AMOUNT)
      .value("NEAREST", vroom::INIT::NEAREST)
      .value("FURTHEST", vroom::INIT::FURTHEST)
      .value("EARLIEST_DEADLINE", vroom::INIT::EARLIEST_DEADLINE)
      .export_values();

  py::enum_<vroom::VIOLATION>(m, "VIOLATION")
      .value("LEAD_TIME", vroom::VIOLATION::LEAD_TIME)
      .value("DELAY", vroom::VIOLATION::DELAY)
      .value("LOAD", vroom::VIOLATION::LOAD)
      .value("MAX_TASKS", vroom::VIOLATION::MAX_TASKS)
      .value("SKILLS", vroom::VIOLATION::SKILLS)
      .value("PRECEDENCE", vroom::VIOLATION::PRECEDENCE)
      .value("MISSING_BREAK", vroom::VIOLATION::MISSING_BREAK)
      .export_values();
}
