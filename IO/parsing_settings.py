""""
The file app.s contains a number of settings that influence the way in which ACE works.

These settings can mainly be divided in two kinds:
    settings that define the language bias (the kind of patterns that can be found),
     and settings that control the system in some other way.

The language bias can be defined in two ways.
1. For beginning users there are the warmode-settings;
    these are simple to use and allow to define a good language bias very quickly.
    warmode-settings are automatically translated by the system to a lower level
        consisting of rmode, type and other settings.
2. The user can also specify the language directly at this lower level, which offers better control of the
way in which the program traverses the search space but is more complicated.
"""
import re
import operator
from functools import reduce
from typing import List
from typing import Optional
from typing import Match

import itertools
from typing import Pattern

from problog.program import PrologFile
from problog.engine import DefaultEngine
from problog.logic import Term

from representation.language import TypeModeLanguage


settings_file_path = 'D:\\KUL\\KUL MAI\\Masterproef\\ACE\\ace\\mach\\examples\\mach.s'


class SettingsParsingError(Exception):
    pass


class Settings:
    def __init__(self):
        self.possible_labels = [] # type: List[Term]
        self.language = TypeModeLanguage(False)

    def add_labels(self, labels: List[Term]):
        self.possible_labels.extend(labels)

    def add_label(self, label: Term):
        self.possible_labels.append(label)


class SettingParser:
    def __init__(self):
        self.classes_parser = ClassesTokenParser()
        type_parser = TypeTokenParser()
        rmode_parser = RmodeTokenParser()

        self.classes_parser.set_successor(type_parser)
        type_parser.set_successor(rmode_parser)

        self.settings = Settings()

    def parse(self, file_path):
        with open(file_path, 'r') as f:
            for line in f:
                self.classes_parser.parse_line(line, self.settings)


class SettingTokenParser:
    """"
    Chain of Responsabiliy Parser
    """
    successor = None  # type: Optional[SettingTokenParser]

    def set_successor(self, successor_parser: 'SettingTokenParser'):
        self.successor = successor_parser

    def can_parse_pre(self, line) -> Match[str]:
        raise NotImplementedError('abstract method')

    def can_parse(self, match: Match[str]) -> bool:
        return match is not None

    def parse_token(self, line: str, settings: Settings, match: Match[str]):
        raise NotImplementedError('abstract method')

    def parse_line(self, line: str, settings: Settings):
        match = self.can_parse_pre(line)
        if self.can_parse(match):
            self.parse_token(line, settings, match)
        elif self.successor is not None:
            self.successor.parse_line(line, settings)


class ClassesTokenParser(SettingTokenParser):
    classes_regex = r'classes\(\[(.*)\]\)\.\n'
    classes_pattern = re.compile(classes_regex) # type: Pattern[str]

    def can_parse_pre(self, line: str) -> Match[str]:
        return self.classes_pattern.search(line)

    def parse_token(self, line: str, settings: Settings, match:Match[str]):
        classes = match.group(1)  # type: str
        classes.replace(' ', '')
        classes = classes.split(',')
        possible_classes = list(map(Term, classes))  # type: List[Term]
        settings.add_labels(possible_classes)


class TypeTokenParser(SettingTokenParser):
    type_regex = r'type\((.*)\).\n'
    type_pattern = re.compile(type_regex)

    conjunction_regex = r'(\w*)\((.*)\)'
    conjunction_pattern = re.compile(conjunction_regex)

    def can_parse_pre(self, line: str) -> Match[str]:
        return self.type_pattern.search(line)

    def parse_token(self, line: str, settings: Settings, match: Match[str]):
        conjunction_definition = match.group(1)
        conjunction_match = self.conjunction_pattern.search(conjunction_definition)
        if conjunction_match is not None:
            functor = conjunction_match.group(1)
            arguments = conjunction_match.group(2)
            arguments.replace(' ', '')
            arguments = arguments.split(',')
            settings.language.add_types(functor, arguments)


class RmodeTokenParser(SettingTokenParser):
    rmode_regex = r'rmode\((.*)\).\n'
    conjunction_regex = r'(\w*)\((.*)\)'

    rmode_pattern = re.compile(rmode_regex)
    conjunction_pattern = re.compile(conjunction_regex)

    arg_regex = r'([+-]{1,3})[A-Z]\w*'
    arg_pattern = re.compile(arg_regex)

    def can_parse_pre(self, line: str) -> Match[str]:
        return self.rmode_pattern.search(line)

    def parse_token(self, line: str, settings: Settings, match: Match[str]):
        conjunction_definition = match.group(1)
        # a conjunction can consist
        conjunction_pattern_match = self.conjunction_pattern.search(conjunction_definition)
        if conjunction_pattern_match is not None:
            functor = conjunction_pattern_match.group(1)
            arguments = conjunction_pattern_match.group(2)
            arguments.replace(' ', '')
            arguments = arguments.split(',')

            all_args_mode_indicators = []
            for argument in arguments:
                arg_match = self.arg_pattern.search(argument)
                if arg_match is not None:
                    mode_indicators = arg_match.group(1)
                    mode_indicators = list(mode_indicators)
                    all_args_mode_indicators.append(mode_indicators)

            total_nb_of_combos = reduce(operator.mul, (list(map(len, all_args_mode_indicators))), 1)
            product = list(itertools.product(*all_args_mode_indicators))
            for combo in product:
                settings.language.add_modes(functor, list(combo))
           # settings.language.add_modes(functor,mode_indicators)


def get_rmode_from_query():
    settings_prolog = PrologFile(settings_file_path)
    # for statement in settings_prolog:
    #     print(statement)
    engine = DefaultEngine()
    # try:
    settings_db = engine.prepare(settings_prolog)
    for statement in settings_db:
        print(statement)
    # except ParseError as perr:
    #     print('ParseError thrown')
    print(engine.query(settings_db, Term('rmode', 'replaceable(+V_0)')))


def main():
    settings_parser = SettingParser()
    settings_parser.parse(settings_file_path)
    print(settings_parser.settings)

if __name__ == "__main__":
    main()
