#!/usr/bin/python

import sys
import os

if sys.version > '3':
    PY3 = True
else:
    PY3 = False

if PY3:
    import subprocess as commands
else:
    import commands
from distutils.core import setup, Extension
from distutils.sysconfig import get_python_lib, get_python_version

if os.path.isfile("MANIFEST"):
    os.unlink("MANIFEST")

# You may have to change these
LUAVERSION = "5.1"
PYTHONVERSION = get_python_version()
PYLIBS = ["python" + get_python_version(), "pthread", "util"]
PYLIBDIR = [get_python_lib(standard_lib=True) + "/config"]
LUALIBS = ["lua" + LUAVERSION]
LUALIBDIR = []
LUAEXE = 'luajit'
LUAINCLUDE = os.path.expanduser("~") + "/torch/install/include"

def pkgconfig(*packages):
    # map pkg-config output to kwargs for distutils.core.Extension
    flag_map = {'-I': 'include_dirs', '-L': 'library_dirs', '-l': 'libraries'}

    for package in packages:
        (pcstatus, pcoutput) = commands.getstatusoutput(
            "pkg-config --libs --cflags %s" % package)
        if pcstatus == 0:
            break
    else:
        sys.exit("pkg-config failed for %s; "
                 "most recent output was:\n%s" %
                 (", ".join(packages), pcoutput))

    kwargs = {}
    for token in pcoutput.split():
        if token[:2] in flag_map:
            kwargs.setdefault(flag_map.get(token[:2]), []).append(token[2:])
        else:                           # throw others to extra_link_args
            kwargs.setdefault('extra_link_args', []).append(token)

    if PY3:
        items = kwargs.items()
    else:
        items = kwargs.iteritems()
    for k, v in items:     # remove duplicated
        kwargs[k] = list(set(v))

    return kwargs

lua_pkgconfig = pkgconfig(LUAEXE, 'lua', 'lua' + LUAVERSION,'python-' + PYTHONVERSION)
lua_pkgconfig['extra_compile_args'] = ['-I'+ LUAINCLUDE]
setup(name="torchpydo",
      version="1.0",
      description="Two-way bridge between Python/Numpy and Lua/Torch",
      author="Wei OUYANG & Jean-michel ARBONA",
      author_email="wei.ouyang@cri-paris.org",
      url="https://github.com/imodpasteur/torchpydo",
      license="LGPLv3",
      long_description="""\
Torchpydo is a two-way bridge between Python/Numpy and Lua/Torch, allowing use using Torch packages(nn, rnn etc.) with numpy inside python. This is a project inspired by lunatic-python and based on lunatic-python.
""",
      packages = ['torchpydo'],
      package_dir = {'':'src'}, 
      ext_modules=[
        Extension("torchpydo.lua-python",
                  ["src/torchpydo/pythoninlua.c", "src/torchpydo/luainpython.c"],
                  **lua_pkgconfig),
        Extension("torchpydo.lua",
                  ["src/torchpydo/pythoninlua.c", "src/torchpydo/luainpython.c"],
                  **lua_pkgconfig),
        ],
      )
