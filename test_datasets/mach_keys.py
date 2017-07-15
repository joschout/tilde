from main.run_keys import run_keys_simpleprogram, run_keys_clausedb

file_name_labeled_examples = 'D:\\KUL\\KUL MAI\\Masterproef\\data\\ACE-examples-data\\ace\\mach\\keys\\mach.kb'
file_name_settings = 'D:\\KUL\\KUL MAI\\Masterproef\\data\\ACE-examples-data\\ace\\mach\\keys\\mach.s'
file_name_background = 'D:\\KUL\\KUL MAI\\Masterproef\\data\\ACE-examples-data\\ace\\mach\\keys\mach.bg'


use_clausedb = False
debug_printing = True
use_mle = True

if use_clausedb:
    run_keys_clausedb(file_name_labeled_examples, file_name_settings, file_name_background, debug_printing=debug_printing, use_mle=use_mle)
else:
    run_keys_simpleprogram(file_name_labeled_examples, file_name_settings, file_name_background, debug_printing=debug_printing, use_mle=use_mle)
