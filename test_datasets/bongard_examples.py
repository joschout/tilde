from main.run_models import run_models_simpleprogram, run_models_clausedb

file_name_settings = 'D:\\KUL\\KUL MAI\\Masterproef\\data\\ACE-examples-data\\ace\\bongard\\examples\\bongard.s'
file_name_labeled_examples = 'D:\\KUL\\KUL MAI\\Masterproef\\data\\ACE-examples-data\\ace\\bongard\\examples\\bongard.kb'


use_clausedb = True
debug_printing = True

if use_clausedb:
    run_models_clausedb(file_name_labeled_examples, file_name_settings, debug_printing=debug_printing)
else:
    run_models_simpleprogram(file_name_labeled_examples, file_name_settings,  debug_printing=debug_printing)
