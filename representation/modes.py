from enum import Enum


class ModeIndicator(Enum):
    INPUT = '+'     # use existing variable
    OUTPUT = '-'    # create new variable (do not reuse existing)
    CONSTANT = 'c'  # insert constant

