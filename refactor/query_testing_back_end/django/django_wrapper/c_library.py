import ctypes

try:
    lib_django = ctypes.CDLL('/home/joschout/Repos/Django-subsumption/lib/libdjango_1_0.so')
except Exception as err:
    lib_django = None