#include <pybind11/iostream.h>
#include <pybind11/pybind11.h>

#include "main.cpp"

namespace py = pybind11;

void init_main(py::module_ &m) {

  m.def(
      "_main",
      [](std::vector<std::string> args) {
        char **argv = new char *[args.size()];
        for (size_t i = 0; i < args.size(); i++) {
          argv[i] = new char[args[i].size() + 1];
          strcpy(argv[i], args[i].c_str());
        }
        py::scoped_ostream_redirect stream(
            std::cout, py::module_::import("sys").attr("stdout"));
        main(args.size(), argv);
      },
      py::arg("args"));
}
