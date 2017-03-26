import re
from typing import Match

from problog.logic import Term
from problog.program import PrologFile, PrologString
from problog.engine import DefaultEngine

from IO.parsing_settings import Settings, SettingParser

file_name_labeled_examples = 'D:\\KUL\\KUL MAI\\Masterproef\\ACE\\ace\\muta\\muta.kb'
file_name_settings = 'D:\\KUL\\KUL MAI\\Masterproef\\ACE\\ace\\muta\\muta.s'
file_name_background = 'D:\\KUL\\KUL MAI\\Masterproef\\ACE\\ace\\muta\\muta.bg'
examples_string = PrologFile(file_name_labeled_examples)


def test():
    test_str = 'predict(machine(+machine,-action)).'
    test = PrologString(test_str)
    engine = DefaultEngine()
    db = engine.prepare(test)
    goals_to_predict = engine.query(db, Term('predict', None))
    print(goals_to_predict)
    print(test)


def test_read_in_keys_examples():
    examples = PrologFile(file_name_labeled_examples)
    for statement in examples:
        key = statement.args[0]
        print(key)


def test_keys_settings_parser():
    setting_parser = SettingParser.get_key_settings_parser()
    setting_parser.parse(file_name_settings)
    print(setting_parser)


def test_background_knowledge():
    background_knowledge = PrologFile(file_name_background)
    for statement in background_knowledge:
        print(statement)

if __name__ == "__main__":
    test()
