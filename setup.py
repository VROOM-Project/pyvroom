from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension, build_ext

extra_compile_args = [
    "-MMD", "-MP", "-std=c++17",
    "-Wextra", "-Wpedantic", "-Wall",
    "-O3", "-DASIO_STANDALONE",
    "-pthread", "-lssl", "-lcrypto",
]

ext_modules = [
    Pybind11Extension(
        "_vroom",
        ["src/_vroom.cpp"],
        include_dirs=["vroom/src"],
        extra_compile_args=extra_compile_args,
    ),
]

setup(
    name="vroom",
    cmdclass={"build_ext": build_ext},
    ext_modules=ext_modules,
    package_dir={"": "src"},
    zip_safe=False,
)
