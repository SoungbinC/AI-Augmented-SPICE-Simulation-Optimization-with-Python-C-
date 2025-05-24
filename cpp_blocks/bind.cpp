#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "rc_filter.cpp"

namespace py = pybind11;

PYBIND11_MODULE(cpp_blocks, m) {
    py::class_<RCFilterBlock>(m, "RCFilterBlock")
        .def(py::init<>())
        .def("set_parameters", &RCFilterBlock::set_parameters)
        .def("simulate", &RCFilterBlock::simulate)
        .def("get_cutoff", &RCFilterBlock::get_cutoff);
}
