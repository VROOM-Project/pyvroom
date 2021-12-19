from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension, build_ext


extra_compile_args = [
    # "-DBOOST_TEST_DYN_LINK",
    # "-DBOOST_SPIRIT_USE_PHOENIX_V3",
    # "-DBOOST_RESULT_OF_USE_DECLTYPE",
    # "-DBOOST_FILESYSTEM_NO_DEPRECATED",
    # "-D USE_LIBOSRM=true",
    # "-D USE_LIBGLPK=true",
    # "-L/usr/local/lib",
    # "-losrm", "-fuse-ld=gold", "-Wl,--disable-new-dtags",
    # "-Wl,--gc-sections", "-Wl,-O1", "-Wl,--hash-style=gnu",
    # "-Wl,--sort-common", "-lboost_system",
    # "-lboost_filesystem", "-lboost_iostreams",
    # "-lboost_thread", "-lrt", "-ltbb", "-lglpk",
]

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
        # extra_objects=glob.glob("vroom/src/**/*.c", recursive=True),
    ),
]

setup(
    name="pyvroom",
    cmdclass={"build_ext": build_ext},
    ext_modules=ext_modules,
    package_dir={"": "src"},
    zip_safe=False,
)
