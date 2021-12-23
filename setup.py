import os
from setuptools import setup, find_packages
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
    name="pyvroom",
    version="0.0.1",
    author="Jonathan Feinberg",
    author_email="jonathf@gmail.com",
    packages=find_packages("src"),
    cmdclass={"build_ext": build_ext},
    install_requires=["numpy"],
    ext_modules=ext_modules,
    package_dir={"": "src"},
    include_dirs=[os.path.join("vroom", "src")],
    zip_safe=False,
)
