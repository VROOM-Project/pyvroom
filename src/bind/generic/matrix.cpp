#include <pybind11/pybind11.h>

#include "structures/generic/matrix.cpp"

namespace py = pybind11;

void init_matrix(py::module_ &m) {

  py::class_<vroom::Matrix<uint32_t>>(m, "Matrix", py::buffer_protocol())
      .def(py::init<std::size_t>(), py::arg("size") = 0)
      .def(py::init([](vroom::Matrix<uint32_t> &m) { return m; }))
      .def(py::init([](const py::buffer &b) {
        py::buffer_info info = b.request();
        if (info.format != py::format_descriptor<uint32_t>::format() ||
            info.ndim != 2 || info.shape[0] != info.shape[1])
          throw std::runtime_error("Incompatible buffer format!");
        auto v = new vroom::Matrix<uint32_t>(info.shape[0]);
        memcpy(v->get_data(), info.ptr,
               sizeof(uint32_t) * (size_t)(v->size() * v->size()));
        return v;
      }))
      .def_buffer([](vroom::Matrix<uint32_t> &m) -> py::buffer_info {
        return py::buffer_info(m.get_data(), sizeof(uint32_t),
                               py::format_descriptor<uint32_t>::format(), 2,
                               {m.size(), m.size()},
                               {sizeof(uint32_t) * m.size(), m.size()});
      })
      .def("get_sub_matrix", &vroom::Matrix<uint32_t>::get_sub_matrix)
      .def("size", &vroom::Matrix<uint32_t>::size);
}
