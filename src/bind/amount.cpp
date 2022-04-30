#include <pybind11/operators.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "structures/vroom/amount.h"

namespace py = pybind11;

void init_amount(py::module_ &m) {

  py::class_<vroom::Amount>(m, "Amount", py::buffer_protocol())
      .def(py::init([](std::size_t size) { return new vroom::Amount(size); }),
           py::arg("size") = 0)
      .def(py::init([](vroom::Amount &a) { return a; }), py::arg("amount"))
      .def(py::init([](const py::buffer &b) {
             py::buffer_info info = b.request();
             if (info.format != py::format_descriptor<int64_t>::format() ||
                 info.ndim != 1)
               throw std::runtime_error("Incompatible buffer format!");
             auto v = new vroom::Amount(info.shape[0]);
             memcpy(v->get_data(), info.ptr,
                    sizeof(int64_t) * (size_t)v->size());
             return v;
           }),
           py::arg("array"))
      .def_buffer([](vroom::Amount &a) -> py::buffer_info {
        return py::buffer_info(a.get_data(), sizeof(int64_t),
                               py::format_descriptor<int64_t>::format(), 1,
                               {a.size()}, {sizeof(int64_t)});
      })
      .def("_lshift", [](const vroom::Amount &a,
                         const vroom::Amount &b) { return a << b; })
      .def("_le", [](const vroom::Amount &a,
                     const vroom::Amount &b) { return a <= b; })
      .def("_push_back", &vroom::Amount::push_back)
      .def("__len__", &vroom::Amount::size);
}
