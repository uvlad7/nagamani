#!/usr/bin/env python

# The MIT License (MIT)

# Copyright (c) 2016 Kenta Murata

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import ctypes.util

# from sysconfig import get_config_var, get_python_version
import os
import sys
import json

is_windows = os.name == "nt"


def linked_libpython():
    return _linked_libpython_windows() if is_windows else _linked_libpython_unix()


def executable():
    return sys.executable


class Dl_info(ctypes.Structure):
    _fields_ = [
        ("dli_fname", ctypes.c_char_p),
        ("dli_fbase", ctypes.c_void_p),
        ("dli_sname", ctypes.c_char_p),
        ("dli_saddr", ctypes.c_void_p),
    ]


def _linked_libpython_unix():
    curr_process = ctypes.CDLL(None)
    curr_process.dladdr.argtypes = [ctypes.c_void_p, ctypes.POINTER(Dl_info)]
    curr_process.dladdr.restype = ctypes.c_int

    dlinfo = Dl_info()
    retcode = curr_process.dladdr(
        ctypes.cast(curr_process.Py_GetVersion, ctypes.c_void_p),
        ctypes.pointer(dlinfo),
    )
    if retcode == 0:  # means error
        return None
    fname = dlinfo.dli_fname.decode()
    # If it's not a shared library
    # it can be 'python' or 'python3' or whatever you use to call python from the shell
    # https://stackoverflow.com/a/41627181/13500870
    if not os.path.exists(fname):
        return None

    path = os.path.realpath(fname)
    if path == os.path.realpath(executable()):
        return None
    return path


def _linked_libpython_windows():
    # Yep, it is implemented, but is not supported
    raise NotImplementedError("Windows is not supported")


try:
    res = {
        "executable": executable(),
        "linked_libpython": linked_libpython(),
    }
    print(json.dumps(res, indent=2))
except Exception as exception:
    sys.exit(f"{exception.__class__.__name__}: {str(exception)}")

# print("linked_libpython: {val}".format(val=(linked_libpython() or "None")))

# sys_keys = [ "executable", "exec_prefix", "prefix" ]

# for var in sys_keys:
#     print("{var}: {val}".format(var=var, val=(getattr(sys, var) or "None")))

# config_keys = [ "INSTSONAME", "LIBDIR", "LIBPL", "LIBRARY", "LDLIBRARY",
#                 "MULTIARCH", "PYTHONFRAMEWORKPREFIX", "SHLIB_SUFFIX", "srcdir" ]

# for var in config_keys:
#     print("{var}: {val}".format(var=var, val=(get_config_var(var) or "None")))

# print("ABIFLAGS: {val}".format(val=get_config_var("ABIFLAGS") or get_config_var("abiflags") or "None"))

# version = get_python_version() or \
#           "{v.major}.{v.minor}".format(v=sys.version_info) or \
#           get_config_var("VERSION")
# print("VERSION: {val}".format(val=version))

# if is_windows:
#     if hasattr(sys, "base_exec_prefix"):
#         PYTHONHOME = sys.base_exec_prefix
#     else:
#         PYTHONHOME = sys.exec_prefix
# else:
#     if hasattr(sys, "base_exec_prefix"):
#         PYTHONHOME = ":".join([sys.base_prefix, sys.base_exec_prefix])
#     else:
#         PYTHONHOME = ":".join([sys.prefix, sys.exec_prefix])
# print("PYTHONHOME: {val}".format(val=PYTHONHOME))
