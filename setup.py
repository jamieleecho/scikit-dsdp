import os
from distutils.core import Extension, setup
from glob import glob

# Modifiy this if BLAS and LAPACK libraries are not in /usr/lib.
BLAS_LIB_DIR = "/usr/lib/libblas/"
LAPACK_LIB_DIR = "/usr/lib/lapack/"

# Default names of BLAS and LAPACK libraries
BLAS_LIB = ["blas"]
LAPACK_LIB = ["lapack"]
BLAS_EXTRA_LINK_ARGS = []

# Set environment variable BLAS_NOUNDERSCORES=1 if your BLAS/LAPACK do
# not use trailing underscores
BLAS_NOUNDERSCORES = False

# Set to 1 if you are installing the DSDP module.
BUILD_DSDP = 1

# Directory containing libraries for DSDP (used only when BUILD_DSDP = 1).
DSDP_LIB_DIR = "/usr/lib"

# Directory containing dsdp5.h (used only when BUILD_DSDP = 1).
DSDP_INC_DIR = "dsdp/C/allinclude"


BLAS_NOUNDERSCORES = (
    int(os.environ.get("DSDP_BLAS_NOUNDERSCORES", BLAS_NOUNDERSCORES)) is True
)
BLAS_LIB = os.environ.get("DSDP_BLAS_LIB", BLAS_LIB)
LAPACK_LIB = os.environ.get("DSDP_LAPACK_LIB", LAPACK_LIB)
BLAS_LIB_DIR = os.environ.get("DSDP_BLAS_LIB_DIR", BLAS_LIB_DIR)
BLAS_EXTRA_LINK_ARGS = os.environ.get("DSDP_BLAS_EXTRA_LINK_ARGS", BLAS_EXTRA_LINK_ARGS)
if type(BLAS_LIB) is str:
    BLAS_LIB = BLAS_LIB.strip().split(",")
if type(LAPACK_LIB) is str:
    LAPACK_LIB = LAPACK_LIB.strip().split(",")
if type(BLAS_EXTRA_LINK_ARGS) is str:
    BLAS_EXTRA_LINK_ARGS = BLAS_EXTRA_LINK_ARGS.strip().split(",")
BUILD_DSDP = int(os.environ.get("PYDSDP_BUILD_DSDP", BUILD_DSDP))
DSDP_LIB_DIR = os.environ.get("PYDSDP_DSDP_LIB_DIR", DSDP_LIB_DIR)
DSDP_INC_DIR = os.environ.get("PYDSDP_DSDP_INC_DIR", DSDP_INC_DIR)

extmods = []

# extension modules

if BUILD_DSDP:
    pydsdp5 = Extension(
        "pydsdp5",
        libraries=LAPACK_LIB + BLAS_LIB,
        include_dirs=["dsdp/C/allinclude"],
        library_dirs=[BLAS_LIB_DIR, LAPACK_LIB_DIR, DSDP_LIB_DIR],
        extra_link_args=BLAS_EXTRA_LINK_ARGS,
        sources=["dsdp/C/pyreadsdpa.c"] + glob("dsdp/C/allc/*.c"),
    )
    extmods += [pydsdp5]

# Setup

setup(
    ext_package="pydsdp",
    ext_modules=extmods,
)
