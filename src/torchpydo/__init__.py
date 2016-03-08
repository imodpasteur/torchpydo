import ctypes
lualib = ctypes.CDLL("/home/wei/torch/install/lib/libluajit.so", mode=ctypes.RTLD_GLOBAL)
import lua
from lua import *

globals_ = None
def update_globals():
    if globals_ is None:
        return
    lg = lua.globals()
    for k in lg:
        ks = str(k)
        if globals_.has_key(ks):
            print("WARNING: variable "+ ks + 'is already exist in python globals, replaced into ' + ks + '_')
            globals_[ks + '_'] = lg[ks]
        else:
            globals_[ks] = lg[ks]

def set_globals(g):
    global globals_
    globals_ = g

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





