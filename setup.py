import os
import platform
from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension, build_ext

extra_compile_args = [
    "-MMD",
    "-MP",
    "-Wextra",
    "-Wpedantic",
    "-Wall",
    "-O3",
    "-DASIO_STANDALONE",
    "-DNDEBUG",
]
extra_link_args=[
    "-lpthread",
    "-lssl",
    "-lcrypto",
]
include_dirs = [os.path.join("vroom", "src")]

if platform.system() == "Darwin":
    # Homebrew places include folders in a weird places.
    include_dirs.append("/usr/local/opt/openssl@1.1/include")
    extra_link_args.insert(0, "-L/usr/local/opt/openssl@1.1/lib")

ext_modules = [
    Pybind11Extension(
        "_vroom",
        [os.path.join("src", "_vroom.cpp")],
        extra_compile_args=extra_compile_args,
        extra_link_args=extra_link_args,
    ),
]

setup(
    cmdclass={"build_ext": build_ext},
    ext_modules=ext_modules,
    include_dirs=include_dirs,
    use_scm_version=True,
)
