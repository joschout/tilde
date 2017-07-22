from IO.parsing_settings import ModelsSettingsParser
from tilde.run.run_models import run_models_simpleprogram, run_models_clausedb

file_name_settings = 'D:\\KUL\\KUL MAI\\Masterproef\\data\\ACE-examples-data\\ace\\mach\\examples\\mach.s'
file_name_background = 'D:\\KUL\\KUL MAI\\Masterproef\\data\\ACE-examples-data\\ace\\mach\\examples\\mach.bg'
file_name_labeled_examples = 'D:\\KUL\\KUL MAI\\Masterproef\\data\\ACE-examples-data\\ace\\mach\\examples\\mach.kb'


use_clausedb = False
debug_printing = True
use_mle = True

parsed_settings = ModelsSettingsParser().parse(file_name_settings)

if use_clausedb:
    run_models_clausedb(file_name_labeled_examples, parsed_settings, file_name_background, debug_printing=debug_printing, use_mle=use_mle)
else:
    run_models_simpleprogram(file_name_labeled_examples, parsed_settings, file_name_background, debug_printing=debug_printing, use_mle=use_mle)
