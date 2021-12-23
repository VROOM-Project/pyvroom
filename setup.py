from setuptools import setup, find_packages
from pybind11.setup_helpers import Pybind11Extension, build_ext

ext_modules = [
    Pybind11Extension(
        "_vroom",
        ["src/_vroom.cpp"],
        include_dirs=[
            "vroom/src",
            # "/usr/include/lua5.2",
            # "/usr/local/include",
            # "/usr/local/include/osrm",
        ],
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
    packages=find_packages(),
    cmdclass={"build_ext": build_ext},
    install_requires=["numpy"],
    ext_modules=ext_modules,
    package_dir={"": "src"},
    zip_safe=False,
)
