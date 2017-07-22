from IO.parsing_settings import KeysSettingsParser
from tilde.run.run_keys import run_keys_clausedb

file_name_labeled_examples = 'D:\\KUL\\KUL MAI\\Masterproef\\data\\ACE-examples-data\\ace\\muta\\muta.kb'
file_name_settings = 'D:\\KUL\\KUL MAI\\Masterproef\\data\\ACE-examples-data\\ace\\muta\\muta.s'
file_name_background = 'D:\\KUL\\KUL MAI\\Masterproef\\data\\ACE-examples-data\\ace\\muta\\muta.bg'


debug_printing = True
use_mle = True

parsed_settings = KeysSettingsParser().parse(file_name_settings)

run_keys_clausedb(file_name_labeled_examples, parsed_settings, file_name_background, debug_printing=debug_printing, use_mle=use_mle)
