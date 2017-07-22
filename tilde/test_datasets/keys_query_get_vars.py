from problog.engine import DefaultEngine
from problog.logic import *

from tilde.IO.parsing_settings import SettingParser
from tilde.IO.parsing_background_knowledge import parse_background_knowledge
from tilde.IO.parsing_examples_keys_format import parse_examples_key_format_with_key

file_name_labeled_examples = 'D:\\KUL\\KUL MAI\\Masterproef\\data\\ACE-examples-data\\ace\\mach\\keys-experimental\\mach.kb'
file_name_settings = 'D:\\KUL\\KUL MAI\\Masterproef\\data\\ACE-examples-data\\ace\\mach\\keys-experimental\\mach.s'
file_name_background = 'D:\\KUL\\KUL MAI\\Masterproef\\data\\ACE-examples-data\\ace\\mach\\keys-experimental\\mach.bg'

setting_parser = SettingParser.get_key_settings_parser()
setting_parser.parse(file_name_settings)


background_knw = parse_background_knowledge(file_name_background)

examples = parse_examples_key_format_with_key(file_name_labeled_examples)

engine = DefaultEngine()
engine.unknown = 1

db = engine.prepare(background_knw)
query_body = Term('machine')(Var('A'), Var('B')) \
             & (Term('worn')(Var('A'), Var('C')) & (Term('not_replaceable')(Var('C'))))
query_head = (Term('predicateToQuery')(Var('A'), Var('C'), Var('B')))
query_rule_for_db = (query_head << query_body)
# db += query

for example in examples:
    db_example = db.extend()
    for statement in example:
        db_example += statement
    db_example += query_rule_for_db
    # for statement in db:
    #     print(statement)
    # for statement in db_example:
    #     print(statement)
    # print("query:", query_rule_for_db)
    example_satisfies_query = engine.query(db_example, query_head)
    print(example_satisfies_query)
