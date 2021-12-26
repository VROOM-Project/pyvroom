import os
from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension, build_ext

ext_modules = [
    Pybind11Extension(
        "_vroom",
        [os.path.join("src", "_vroom.cpp")],
        extra_compile_args=[
            "-MMD",
            "-MP",
            "-Wextra",
            "-Wpedantic",
            "-Wall",
            "-O3",
            "-DASIO_STANDALONE",
            "-DNDEBUG",
        ],
        extra_link_args=[
            "-lpthread",
            "-lssl",
            "-lcrypto",
        ],
    ),
]

setup(
    cmdclass={"build_ext": build_ext},
    ext_modules=ext_modules,
    include_dirs=[os.path.join("vroom", "src")],
    use_scm_version = True,
)
