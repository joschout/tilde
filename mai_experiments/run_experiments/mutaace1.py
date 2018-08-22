import os

import sys

from mai_version.fold.fold_file_parser import main_cross_validation
from mai_version.main import kb_suffix, s_suffix, bg_suffix

# CHANGE THESE TWO FOR EACH TEST
test_name = 'mutaace1'
logic_name = 'muta-d'

# --- command-line printing settings ---
debug_printing_tree_building = False
debug_printing_program_conversion = False
debug_printing_get_classifier = False
debug_printing_classification = False

filter_out_unlabeled_examples = False
hide_printouts = True

# --- directories ---
droot = 'D:\\KUL\\KUL MAI\\Masterproef\\TILDE\\tilde\\fold\\data\\'
dlogic_relative = 't-0-0-0\\'
dfold_relative = 'folds\\'
dout_relative = 'output\\'

dlogic = droot + test_name + '\\' + dlogic_relative
dfold = droot + test_name + '\\' + dfold_relative
doutput = droot + test_name + '\\' + dout_relative

# --- file names ---
fname_examples = dlogic + logic_name + kb_suffix
fname_settings = dlogic + logic_name + s_suffix
fname_background = dlogic + logic_name + bg_suffix

# --- fold settings ---
fname_prefix_fold = 'test'
fold_start_index = 0
nb_folds = 10
fold_suffix = '.txt'

# -- create output directory
if not os.path.exists(doutput):
    os.makedirs(doutput)

print("start mutaace1")
save_stdout = sys.stdout
if hide_printouts:
    sys.stdout = open(os.devnull, "w")

main_cross_validation(fname_examples=fname_examples, fname_settings=fname_settings, fname_background=fname_background,
                      dir_fold_files=dfold, fname_prefix_fold=fname_prefix_fold, fold_start_index=fold_start_index,
                      nb_folds=nb_folds, fold_suffix=fold_suffix, dir_output_files=doutput,
                      filter_out_unlabeled_examples=filter_out_unlabeled_examples,
                      debug_printing_tree_building=debug_printing_tree_building,
                      debug_printing_program_conversion=debug_printing_program_conversion,
                      debug_printing_get_classifier=debug_printing_get_classifier,
                      debug_printing_classification=debug_printing_classification)
if hide_printouts:
    sys.stdout = save_stdout
print("finished mutaace1")