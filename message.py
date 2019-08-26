from ctypes import *

class message(Structure):
    _fields_ = [("id", c_uint32),
                ("counter", c_uint32),
                ("opcode", c_uint32)]


