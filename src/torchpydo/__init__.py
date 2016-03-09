import os
import ctypes
lualib = ctypes.CDLL(os.path.expanduser("~") + "/torch/install/lib/libluajit.so", mode=ctypes.RTLD_GLOBAL)
import lua
from lua import *
import inspect

globals_ = None
builtins_ = None
warningList = []
def update_globals():
    if globals_ is None:
        return
    lg = lua.globals()
    for k in lg:
        ks = str(k)
        if ks in builtins_ or globals_.has_key(ks):
            if ks in builtins_ or inspect.ismodule(globals_[ks]):
                if not ks in warningList:
                    warningList.append(ks)
                    print('WARNING: variable "'+ ks + '" is already exist in python, use "' + ks + '_" to refer to the lua version')
                globals_[ks + '_'] = lg[ks]
                continue
        globals_[ks] = lg[ks]

def set_globals(g, bi):
    global globals_,builtins_,warningList
    warningList = []
    builtins_ = dir(bi)
    globals_ = g
    update_globals()
    
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





