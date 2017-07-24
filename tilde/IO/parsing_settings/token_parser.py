import itertools
import re
from typing import List
from typing import Match
from typing import Optional
from typing import Pattern

from problog.logic import Term

from tilde.IO.parsing_settings.utils import Settings, SettingsParsingError, KeysPredictionGoalHandler, \
    ConstantBuilder


class SettingTokenParser:
    """"
    Chain of Responsibility Parser
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
