from machine_examples import *
from test2 import getLabel

examples = [ex1, ex2, ex3, ex4, ex5, ex6, ex7, ex8, ex9, ex10]


labels = getLabel(examples, rules)
print(labels)