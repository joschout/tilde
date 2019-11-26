import os

import matplotlib
matplotlib.use('Agg')
import statistics
import timeit
from mai_version.utils import block_all_printouts, enable_printouts
# # import gc
#
# block_all_printouts()
import matplotlib.pyplot as plt2

from mai_version.IO.parsing_settings.setting_parser import KeysSettingsParser
from mai_version.representation.example import InternalExampleFormat
from mai_version.run.run_keys import run_keys
from mai_version.trees.TreeBuilder import TreeBuilderType

project_dir = '/home/joschout/Repos/tilde'

dataset_name = 'bongard'
data_dir = os.path.join(project_dir, 'ACE-examples-data', dataset_name)

file_name_settings = os.path.join(data_dir, 'keys', dataset_name + '.s')
file_name_labeled_examples = os.path.join(data_dir, 'keys', dataset_name + '.kb')


use_clausedb = True

debug_printing_example_parsing = False
debug_printing_tree_building = False
debug_printing_tree_pruning = False
debug_printing_program_conversion = True
debug_printing_get_classifier = False
debug_printing_classification = False

parsed_settings = KeysSettingsParser().parse(file_name_settings)

treebuilder_type = TreeBuilderType.DETERMINISTIC

if use_clausedb:
    internal_ex_format = InternalExampleFormat.CLAUSEDB
else:
    internal_ex_format = InternalExampleFormat.SIMPLEPROGRAM


times = []
#
for i in range(0, 10):
#
    start = timeit.default_timer()

    run_keys(file_name_labeled_examples, parsed_settings, internal_ex_format, treebuilder_type,
             debug_printing_example_parsing=debug_printing_example_parsing,
             debug_printing_tree_building=debug_printing_tree_building,
             debug_printing_tree_pruning=debug_printing_tree_pruning,
             debug_printing_program_conversion=debug_printing_program_conversion,
             debug_printing_get_classifier=debug_printing_get_classifier,
             debug_printing_classification=debug_printing_classification
             )
#     gc.collect()
    end = timeit.default_timer()


# print("time", end - start)

    times.append(end-start)
# enable_printouts()
print("times:", times)
print("average duration:", statistics.mean(times), "seconds")
plt2.clf()
plt2.plot(times, 'ro')
plt2.ylabel('seconds')
plt2.xlabel('iteration')
plt2.title("total run time")
plt2.savefig("total_run_time.png")
