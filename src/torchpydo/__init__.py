import os
import ctypes
lualib = ctypes.CDLL(os.path.expanduser("~") + "/torch/install/lib/libluajit.so", mode=ctypes.RTLD_GLOBAL)
import lua
from lua import *
import inspect

globals_ = None
def update_globals(enable_warning=False):
    if globals_ is None:
        return
    lg = lua.globals()
    for k in lg:
        ks = str(k)
        if globals_.has_key(ks):
            if inspect.ismodule(globals_[ks]):
                if enable_warning:
                    print("WARNING: variable "+ ks + ' is already exist in python globals, use ' + ks + '_ to refer to the lua version')
                globals_[ks + '_'] = lg[ks]
                continue
        globals_[ks] = lg[ks]

def set_globals(g):
    global globals_
    globals_ = g
    update_globals(True)
    
eval_ = lua.eval
def eval(cmd):
    ret = eval_(cmd)
    update_globals()
    return ret

execute_ = lua.execute
def execute(cmd):
    ret = execute_(cmd)
    update_globals()
    return ret

require_ = lua.require
def require(module_name):
    ret = require_(module_name)
    update_globals()
    return ret

def boostrap_self(obj,func_name):
    '''
        bootstrap a function to add self as the first argument
    '''
    if obj[func_name+'_']:
        return
    func = obj[func_name]
    def func_self(*opt):
        func(obj,*opt)
    obj[func_name+'_'] = func
    obj[func_name] = func_self

bs = boostrap_self





