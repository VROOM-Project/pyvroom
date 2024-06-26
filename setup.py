import json
import logging
import os
import platform
from subprocess import run
from pathlib import Path
from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension, build_ext

include_dirs = [
    "src",
    os.path.join("vroom", "src"),
    os.path.join("vroom", "include"),
    os.path.join("vroom", "include", "cxxopts", "include"),
]
libraries = []
library_dirs = []

if platform.system() == "Windows":
    extra_compile_args = [
        "-DNOGDI",
        "-DNOMINMAX",
        "-DWIN32_LEAN_AND_MEAN",
        "-DASIO_STANDALONE",
        "-DUSE_PYTHON_BINDINGS",
        "-DUSE_ROUTING=true"
    ]
    extra_link_args = []

else:  # anything *nix
    extra_compile_args = [
        "-MMD",
        "-MP",
        "-Wextra",
        "-Wpedantic",
        "-Wall",
        "-O3",
        "-DASIO_STANDALONE",
        "-DNDEBUG",
        "-DUSE_PYTHON_BINDINGS",
        "-DUSE_ROUTING=true"
    ]
    extra_link_args = [
        "-lpthread",
        "-lssl",
        "-lcrypto",
    ]

    if platform.system() == "Darwin":
        # Homebrew puts include folders in weird places.
        prefix = run(["brew", "--prefix"], capture_output=True).stdout.decode("utf-8")[:-1]
        include_dirs.append(f"{prefix}/opt/openssl@1.1/include")
        include_dirs.append(f"{prefix}/include")
        extra_link_args.insert(0, f"-L{prefix}/lib")
        extra_link_args.insert(0, f"-L{prefix}/opt/openssl@1.1/lib")

# try conan dependency resolution
conanfile = tuple(Path(__file__).parent.resolve().rglob("conanbuildinfo.json"))
if conanfile:
    logging.info("Using conan to resolve dependencies.")
    with conanfile[0].open() as f:
        conan_deps = json.load(f)["dependencies"]
    for dep in conan_deps:
        include_dirs.extend(dep["include_paths"])
        libraries.extend(dep["libs"])
        libraries.extend(dep["system_libs"])
        library_dirs.extend(dep["lib_paths"])
else:
    logging.warning("Conan not installed and/or no conan build detected. Assuming dependencies are installed.")

ext_modules = [
    Pybind11Extension(
        "_vroom",
        [os.path.join("src", "_vroom.cpp")],
        library_dirs=library_dirs,
        libraries=libraries,
        extra_compile_args=extra_compile_args,
        extra_link_args=extra_link_args,
    ),
]

setup(
    cmdclass={"build_ext": build_ext},
    ext_modules=ext_modules,
    ext_package="vroom",
    include_dirs=include_dirs,
    use_scm_version=True,
    entry_points={"console_scripts": ["vroom=vroom:main"]},
)
