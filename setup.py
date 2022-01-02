import json
import os
import platform
from pathlib import Path
from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension, build_ext

extra_link_args = [
    "-lpthread",
    "-lssl",
    "-lcrypto",
]
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
include_dirs = [os.path.join("vroom", "src")]
libraries = []
library_dirs = []

# try conan dependency resolution
conanfile = tuple(Path().rglob('conanbuildinfo.json'))
if conanfile:
    print("INFO: Using conan to resolve dependencies.")
    with open(conanfile[0]) as f:
        conan_deps = json.load(f)['dependencies']
    for dep in conan_deps:
        include = dep['include_paths']
        libraries = dep['lib_paths']

        include_dirs.extend(include)
        if libraries:
            library_dirs.extend(libraries)
else:
    print('WARN: Conan not installed and/or no conan build detected. Assuming dependencies are installed.')

if platform.system() == "Darwin":
    # Homebrew puts include folders in weird places.
    include_dirs.append("/usr/local/opt/openssl@1.1/include")
    extra_link_args.insert(0, "-L/usr/local/opt/openssl@1.1/lib")
elif platform.system() == "Windows":
    extra_compile_args = ["-DNOGDI", "-DNOMINMAX", "-DASIO_STANDALONE"]
    extra_link_args = []

ext_modules = [
    Pybind11Extension(
        "_vroom",
        [os.path.join("src", "_vroom.cpp")],
        library_dirs=library_dirs,
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
