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
from typing import List, Tuple
from typing import Optional
from typing import Match

import itertools
from typing import Pattern

from problog.program import PrologFile
from problog.engine import DefaultEngine
from problog.logic import Term, Constant, Var

from classification.classification_helper import Label
from problog_helper.problog_helper import apply_substitution_to_term
from representation.language import TypeModeLanguage


class SettingsParsingError(Exception):
    pass


class ConstantBuilder:
    @staticmethod
    def parse_constant_str(constant_str: str) -> Constant:
        if ConstantBuilder.is_int(constant_str):
            return Constant(int(constant_str))
        elif ConstantBuilder.is_float(constant_str):
            return Constant(float(constant_str))
        else:
            return Term(constant_str)

    @staticmethod
    def is_float(x: str) -> bool:
        try:
            a = float(x)
        except ValueError:
            return False
        else:
            return True

    @staticmethod
    def is_int(x: str) -> bool:
        try:
            a = float(x)
            b = int(a)
        except ValueError:
            return False
        else:
            return a == b


class KeysPredictionGoalHandler:
    def __init__(self, functor, modes, types):
        self.functor = functor  # type: str
        self.modes = modes  # type: List[str]
        self.types = types  # type: List[str]

    def get_prediction_goal(self) -> Term:
        prediction_goal_term = Term(self.functor)

        nb_of_args = len(self.modes)
        arguments = [Var('#')] * nb_of_args
        prediction_goal_term = prediction_goal_term(*arguments)

        prediction_goal_term = prediction_goal_term.apply(TypeModeLanguage.ReplaceNew(0))
        return prediction_goal_term

    def get_predicate_goal_index_of_label_var(self) -> int:
        for index, arg_mode in enumerate(self.modes):
            if arg_mode == "-":
                return index
        raise SettingsParsingError("predicate to predict has no argument with arg_mode '-'")


class Settings:
    def __init__(self):
        self.possible_labels = []  # type: List[Label]
        self.language = TypeModeLanguage(False)
        self.is_typed = None  # type: Optional[bool]
        self.prediction_goal_handler = None  # type: KeysPredictionGoalHandler

    def add_labels(self, labels: List[Label]):
        self.possible_labels.extend(labels)

    def add_label(self, label: Label):
        self.possible_labels.append(label)

    def get_prediction_goal_handler(self) -> KeysPredictionGoalHandler:
        return self.prediction_goal_handler


class SettingParser:
    def __init__(self):
        self.first_setting_token_parser = None
        self.settings = Settings()

    def parse(self, file_path):
        if self.first_setting_token_parser is not None:
            with open(file_path, 'r') as f:
                for line in f:
                    self.first_setting_token_parser.parse_line(line, self.settings)
        else:
            raise SettingsParsingError("No SettingTokenParser set as first token parser")

    @staticmethod
    def get_models_settings_parser() -> 'SettingParser':
        setting_parser = SettingParser()
        classes_token_parser = ClassesTokenParser()
        type_token_parser = TypeTokenParser()
        rmode_token_parser = RmodeTokenParser()

        setting_parser.first_setting_token_parser = classes_token_parser
        classes_token_parser.set_successor(type_token_parser)
        type_token_parser.set_successor(rmode_token_parser)
        return setting_parser

    @staticmethod
    def get_key_settings_parser() -> 'SettingParser':
        setting_parser = SettingParser()
        prediction_token_parser = PredictionTokenParser()
        type_token_parser = TypeTokenParser()
        rmode_token_parser = RmodeTokenParser()

        setting_parser.first_setting_token_parser = prediction_token_parser
        prediction_token_parser.set_successor(type_token_parser)
        type_token_parser.set_successor(rmode_token_parser)
        return setting_parser

    @staticmethod
    def get_settings_keys_format( file_path:str) -> Settings:
        setting_parser = SettingParser.get_key_settings_parser()
        setting_parser.parse(file_path)
        return setting_parser.settings

    @staticmethod
    def get_settings_models_format(file_path: str) -> Settings:
        setting_parser = SettingParser.get_models_settings_parser()
        setting_parser.parse(file_path)
        return setting_parser.settings


class SettingTokenParser:
    """"
    Chain of Responsabiliy Parser
    """
    successor = None  # type: Optional[SettingTokenParser]

    def set_successor(self, successor_parser: 'SettingTokenParser'):
        self.successor = successor_parser

    def can_parse_pre(self, line) -> Optional[Match[str]]:
        raise NotImplementedError('abstract method')

    @staticmethod
    def can_parse(match: Optional[Match[str]]) -> bool:
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
    classes_regex = r'classes\(\[(.*)\]\)\.'
    classes_pattern = re.compile(classes_regex)  # type: Pattern[str]

    def can_parse_pre(self, line: str) -> Optional[Match[str]]:
        return self.classes_pattern.match(line)

    def parse_token(self, line: str, settings: Settings, match: Match[str]):
        classes = match.group(1)  # type: str
        classes = classes.replace(' ', '')
        classes = classes.split(',')
        possible_classes = list(map(Term, classes))  # type: List[Term]
        settings.add_labels(possible_classes)


class TypedLanguageTokenParser(SettingTokenParser):
    typed_language_regex = r'typed_language\((\s*yes\s*|\s*no\s*)\).'
    typed_language_pattern = re.compile(typed_language_regex)

    def can_parse_pre(self, line: str) -> Optional[Match[str]]:
        return self.typed_language_pattern.match(line)

    def parse_token(self, line: str, settings: Settings, match: Match[str]):
        typed = match.group(1)
        typed = typed.replace(' ', '')
        if typed == 'yes':
            settings.is_typed = True
        elif typed == 'no':
            settings.is_typed = False
        else:
            raise SettingsParsingError("invalid setting line: " + line)


class PredictionTokenParser(SettingTokenParser):
    predict_regex = r'predict\((.*)\)\.'
    predict_pattern = re.compile(predict_regex)

    conjunction_regex = r'(\w*)\((.*)\)'
    conjunction_pattern = re.compile(conjunction_regex)

    argument_regex = '([+-])(\w*)'
    argument_pattern = re.compile(argument_regex)

    def can_parse_pre(self, line: str) -> Optional[Match[str]]:
        return self.predict_pattern.match(line)

    def parse_token(self, line: str, settings: Settings, match: Match[str]):
        # TODO: change on typed language or not
        # TODO: for now, assume the language is completely typed

        prediction_goal = match.group(1)
        conjunction_match = self.conjunction_pattern.search(prediction_goal)
        if conjunction_match is not None:
            # TODO: change this from literal to conjunction
            functor = conjunction_match.group(1)
            arguments = conjunction_match.group(2)
            arguments = arguments.replace(' ', '')
            arguments = arguments.split(',')
            modes = []
            types = []

            for argument in arguments:
                moded_arg_match = self.argument_pattern.match(argument)
                if moded_arg_match is not None:
                    # mode can only be + or -
                    mode = moded_arg_match.group(1)
                    type = moded_arg_match.group(2)
                    modes.append(mode)
                    types.append(type)
                else:
                    raise SettingsParsingError("invalid setting line: " + line)

            # some might be typed, some might not be
            # check if all args are typed or untyped
            list_args_is_typed = list(map(lambda arg_type: True if arg_type is not '' else False, types))
            have_all_args_type_specified = all(list_args_is_typed)
            have_some_args_type_specified = any(list_args_is_typed)
            if not have_all_args_type_specified and have_some_args_type_specified:
                raise SettingsParsingError('the predicted conjunction has to be completely typed or completely untyped')
            settings.language.add_types(functor, types)
            # TODO: think about this, I don't think it needs to be added to the possible refinement conjunctions
            # settings.language.add_modes(functor, modes)
            settings.prediction_goal_handler = KeysPredictionGoalHandler(functor, modes, types)
        else:
            raise SettingsParsingError("invalid setting line: " + line)


class TypeTokenParser(SettingTokenParser):
    type_regex = r'type\((.*)\).'
    type_pattern = re.compile(type_regex)

    conjunction_regex = r'(\w*)\((.*)\)'
    conjunction_pattern = re.compile(conjunction_regex)

    def can_parse_pre(self, line: str) -> Optional[Match[str]]:
        return self.type_pattern.match(line)

    def parse_token(self, line: str, settings: Settings, match: Match[str]):
        conjunction_definition = match.group(1)
        conjunction_match = self.conjunction_pattern.search(conjunction_definition)
        if conjunction_match is not None:
            functor = conjunction_match.group(1)
            arguments = conjunction_match.group(2)
            arguments = arguments.replace(' ', '')
            arguments = arguments.split(',')
            settings.language.add_types(functor, arguments)


class RmodeTokenParser(SettingTokenParser):
    rmode_regex = r'rmode\((.*)\).'
    rmode_pattern = re.compile(rmode_regex)

    conjunction_regex = r'(\w*)\((.*)\)'
    conjunction_pattern = re.compile(conjunction_regex)

    moded_var_regex = r'([+-]{1,3})[A-Z]\w*'
    moded_var_pattern = re.compile(moded_var_regex)

    const_gen_regex = r'#\[(.*)\]'
    const_gen_pattern = re.compile(const_gen_regex)

    def can_parse_pre(self, line: str) -> Optional[Match[str]]:
        return self.rmode_pattern.match(line)

    def parse_token(self, line: str, settings: Settings, match: Match[str]):
        conjunction_definition = match.group(1)
        # a conjunction can consist
        conjunction_pattern_match = self.conjunction_pattern.search(conjunction_definition)
        if conjunction_pattern_match is not None:
            functor = conjunction_pattern_match.group(1)
            arguments = conjunction_pattern_match.group(2)
            arguments = arguments.replace(' ', '')
            arguments = self.__tokenize_rmode_argument_string(arguments)

            self._parse_rmode_arguments(arguments, functor, settings)

    def _parse_rmode_arguments(self, arguments: List[str], functor: str, settings: Settings):
        all_args_mode_indicators = []
        for argument_index, argument in enumerate(arguments):
            moded_var_match = self.moded_var_pattern.search(argument)
            # checking if the current argument is a moded variable
            if moded_var_match is not None:
                mode_indicators = moded_var_match.group(1)
                mode_indicators = list(mode_indicators)
                all_args_mode_indicators.append(mode_indicators)
            else:
                const_gen_match = self.const_gen_pattern.search(argument)
                # checking of the current argument is a list defining the possible values for this arg
                if const_gen_match is not None:
                    constants_str = const_gen_match.group(1)  # type: str
                    constants_str = constants_str.split(',')
                    constants = [ConstantBuilder.parse_constant_str(const_str) for const_str in constants_str]
                    # add a special mode indicator, cfr 'c'
                    # add the constants to the language
                    all_args_mode_indicators.append(['c'])
                    const_type = functor + '_' + str(argument_index)
                    settings.language.add_values(const_type, *constants)

        # total_nb_of_combos = reduce(operator.mul, (list(map(len, all_args_mode_indicators))), 1)
        product = list(itertools.product(*all_args_mode_indicators))
        for combo in product:
            settings.language.add_modes(functor, list(combo))
            # settings.language.add_modes(functor,mode_indicators)

    def __tokenize_rmode_argument_string(self, args: str) -> List[str]:
        """
        Breaks the arguments of an rmode line into substrings. This has to handle the case where there is a list of possible values.
        For example:    rmode(5: config(+P,+S,#[up,down])).    
        --> input of this method: '+P,+S,#[up,down]'
            output:     ['+P', '+S', '#[up,down]']   
        :param args: 
        :return: 
        """
        if args == '':
            return []
        open_bracket_index = args.find('#[')
        if open_bracket_index == -1:  # no open bracket found
            arguments = args.split(',')
        else:
            if open_bracket_index == 0:
                arguments = []
            else:
                arguments = args[0:open_bracket_index - 1].split(',')

            close_bracket_index = args.index(']')
            arguments.append(args[open_bracket_index:close_bracket_index + 1])

            if close_bracket_index + 2 <= len(args):
                args_after = self.__tokenize_rmode_argument_string(args[close_bracket_index + 2:])
                arguments.extend(args_after)
        return arguments

    def parse_token_experimental(self, line: str, settings: Settings, match: Match[str]):
        pass


# def get_rmode_from_query():
#     settings_prolog = PrologFile(settings_file_path)
#     # for statement in settings_prolog:
#     #     print(statement)
#     engine = DefaultEngine()
#     # try:
#     settings_db = engine.prepare(settings_prolog)
#     for statement in settings_db:
#         print(statement)
#     # except ParseError as perr:
#     #     print('ParseError thrown')
#     print(engine.query(settings_db, Term('rmode', 'replaceable(+V_0)')))
