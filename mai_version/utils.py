import warnings
import functools

import time

import sys
import os


def deprecated(func):
    """This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emmitted
    when the function is used."""

    @functools.wraps(func)
    def new_func(*args, **kwargs):
        warnings.simplefilter('always', DeprecationWarning)  # turn off filter
        warnings.warn("Call to deprecated function {}.".format(func.__name__), category=DeprecationWarning,
                      stacklevel=2)
        warnings.simplefilter('default', DeprecationWarning)  # reset filter
        return func(*args, **kwargs)

    return new_func


class Timer:
    def __init__(self, name=None):
        self.name = name
        self.start_time = None
        self.end_time = None

    def start(self) -> None:
        self.start_time = time.time()

    def end(self) -> float:
        self.end_time = time.time()
        return self.end_time


def block_all_printouts():
    sys.stdout = open(os.devnull, "w")


def enable_printouts():
    sys.stdout = sys.__stdout__
