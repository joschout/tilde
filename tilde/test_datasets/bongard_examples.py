from IO.parsing_settings import ModelsSettingsParser
from tilde.run.run_models import run_models_simpleprogram, run_models_clausedb

file_name_settings = 'D:\\KUL\\KUL MAI\\Masterproef\\data\\ACE-examples-data\\ace\\bongard\\examples\\bongard.s'
file_name_labeled_examples = 'D:\\KUL\\KUL MAI\\Masterproef\\data\\ACE-examples-data\\ace\\bongard\\examples\\bongard.kb'


use_clausedb = True
debug_printing = True

parsed_settings = ModelsSettingsParser().parse(file_name_settings)

if use_clausedb:
    run_models_clausedb(file_name_labeled_examples, parsed_settings, debug_printing=debug_printing)
else:
    run_models_simpleprogram(file_name_labeled_examples, parsed_settings,  debug_printing=debug_printing)
