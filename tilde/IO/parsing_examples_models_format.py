""""
Parsing examples in the MODELS format.


The knowledge base is assumed to be in the les app.kb (which should contain example-related
information) and app.bg (which should contain background knowledge about the domain). A predicate
or relation can be considered to be background knowledge if adding an example to the set of examples
does not change the denition of that predicate.

There are two different formats available for the knowledge base.

In one format, which we call the
models format, each individual example is described by a so-called model, a block beginning with
begin(model(name)) and ending with end(model(name)). All facts in between the model delimiters
are considered to describe properties of the single example.

The second format, which we refer to as the key format, is closer to normal Prolog syntax and can
actually be seen as just a Prolog program. In this format, there is a less clear distinction between
example descriptions and background knowledge. Individual examples are referred to by a certain
identifier, and properties of a single example are given by listing facts that refer to this identifier.

"""
import re
from typing import List, Tuple, Pattern, Dict
from typing import Optional, Iterable

from problog.logic import Term

from tilde.IO.parsing_settings.utils import ConstantBuilder
from tilde.problog_helper.problog_helper import get_probability
from tilde.representation.example import PrologStringExample

begin_model_regex = r'begin\(model\((\d+)\)\)\.\n'
end_model_regex = r'end\(model\((\d+)\)\)\.\n'

begin_pattern = re.compile(begin_model_regex)
end_pattern = re.compile(end_model_regex)


class ExampleParseException(Exception):
    pass


    # def parse_examples_model_format(file_name_labeled_examples: str, possible_labels=None) -> Iterable[LogicProgram]:
    #     examples_found = []  # type: LogicProgram
    #
    #     label_patterns = get_label_patterns_methods_format(possible_labels)  # type: List[Tuple[Term, Pattern[str]]]
    #
    #     with open(file_name_labeled_examples, 'r') as f:
    #         parsing_example = False
    #         digit = None  # type: Optional(int)
    #
    #         prolog_string_accumulator = ''
    #         example_labels = set()
    #
    #         for line in f:
    #             result_of_pattern_matching = None
    #             if not parsing_example:  # no unclosed parameter delimiters
    #                 result_of_pattern_matching = begin_pattern.search(line)
    #                 # search for the begin(model(digits)). delimiter
    #
    #                 # if we have found the beginning delimiter of an example
    #                 if result_of_pattern_matching is not None:
    #                     digit = result_of_pattern_matching.group(1)
    #                     parsing_example = True
    #                     prolog_string_accumulator = ''
    #                     example_labels = set()
    #                 else:
    #                     pass
    #             else:  # parsing an example, i.e. an open begin(model(digit)). is still unclosed
    #                 result_of_pattern_matching = end_pattern.search(line)
    #                 if result_of_pattern_matching is not None:
    #                     end_digit = result_of_pattern_matching.group(1)
    #                     if digit != end_digit:
    #                         raise ExampleParseException("The example number in the begin and end tags do not match")
    #                     else:
    #                         parsing_example = False
    #
    #                         example = parse_example_string(prolog_string_accumulator, example_labels)
    #                         examples_found.append(example)
    #
    #                 else:
    #                     current_line_is_label = False
    #                     matches_label = None
    #                     for label, label_pattern in label_patterns:
    #                         matches_label = label_pattern.search(line)
    #                         if matches_label is not None:
    #                             example_labels.add(label)
    #                             current_line_is_label = True
    #                     if current_line_is_label is False:
    #                         prolog_string_accumulator = prolog_string_accumulator + line
    #     return examples_found

Probability = float

class ModelsExampleParser:
    def __init__(self, possible_labels: Optional[Iterable[Term]] = None):
        self.label_patterns = self._get_label_patterns(possible_labels)  # List[Tuple[Term, Pattern[str]]]
        self.examples_found = []  # type: List[PrologStringExample]

        self.currently_parsing_example = False  # type: bool
        self.id_of_current_example = None  # type: Optional(str)
        self.labels_of_current_example = None  # type: Optional[Dict[Term, Probability]]
        self.prolog_string_accumulator = None  # type: Optional(str)

    def _parse_examples_model_format(self, file_name_labeled_examples: str):
        with open(file_name_labeled_examples, 'r') as f:
            for line in f:
                if not self.currently_parsing_example:  # no unclosed parameter delimiters
                    self._parse_line_check_if_it_begins_a_new_example(line)
                else:  # parsing an example, i.e. an open begin(model(digit)). is still unclosed
                    self._parse_example_line(line)

    def _parse_line_check_if_it_begins_a_new_example(self, line: str):
        matches_begin_of_example = begin_pattern.search(line)
        # search for the begin(model(digits)). delimiter

        # if we have found the beginning delimiter of an example
        if matches_begin_of_example is not None:
            self.currently_parsing_example = True
            self.id_of_current_example = matches_begin_of_example.group(1)
            self.labels_of_current_example = dict()
            self.prolog_string_accumulator = ''
        else:
            pass

    def _parse_example_line(self, line: str):
        # parsing an example, i.e. an open begin(model(digit)). is still unclosed
        matches_end_of_example = end_pattern.search(line)
        if matches_end_of_example is not None:
            self._parse_example_end_line(matches_end_of_example.group(1))
        else:
            current_line_is_label = self._check_and_parse_if_line_is_a_label(line)
            if not current_line_is_label:
                self.prolog_string_accumulator = self.prolog_string_accumulator + line

    def _parse_example_end_line(self, example_id_on_end_line: str):
        if self.id_of_current_example != example_id_on_end_line:
            raise ExampleParseException("The example number in the begin and end tags do not match")
        else:
            example = self._parse_example_string(self.prolog_string_accumulator)
            example = self._add_example_info(example, self.labels_of_current_example, self.id_of_current_example)

            self.examples_found.append(example)

            self.currently_parsing_example = False
            self.id_of_current_example = None
            self.labels_of_current_example = None
            self.prolog_string_accumulator = None

    def _check_and_parse_if_line_is_a_label(self, line: str) -> bool:
        current_line_is_label = False
        for label, label_pattern in self.label_patterns:  # type: Tuple[Term, Pattern[str]]
            matches_label = label_pattern.search(line)
            if matches_label is not None:
                parsed_label = Term.from_string(line)
                self.labels_of_current_example[parsed_label] = get_probability(parsed_label)
                current_line_is_label = True
        return current_line_is_label

    @staticmethod
    def _get_label_patterns(possible_labels: Optional[Iterable[Term]]) -> List[Tuple[Term, Pattern[str]]]:
        # getting regex patterns for all possible labels
        label_patterns = []  # type: List[Tuple[Term, Pattern[str]]]
        if possible_labels is not None:
            for possible_label in possible_labels:
                label_pattern_string = r'(([-+]?[0-9]*\.?[0-9]+)::)?' + str(possible_label) + '.\n'
                label_patterns.append((possible_label, re.compile(label_pattern_string)))
        return label_patterns

    @staticmethod
    def _parse_example_string(prolog_string_unlabeled: str) -> PrologStringExample:
        return PrologStringExample(prolog_string_unlabeled)


    @staticmethod
    def _add_example_info(example: PrologStringExample, example_labels:Optional[Dict[Term, Probability]]=None, example_id_str:Optional[str]=None)->PrologStringExample:
        # if it has one or more labels, add them
        if example_labels is not None:
            if len(example_labels) == 1:
                #TODO: Note, value of probability is never used
                label, probability = example_labels.popitem()
                example.label = label
            else:
                example.label = example_labels

        # add its key
        example.key = ConstantBuilder.parse_constant_str(example_id_str)

        return example

    @staticmethod
    def parse(file_name_labeled_examples: str, possible_labels: Optional[Iterable[Term]] = None) -> List[
        PrologStringExample]:
        example_parser = ModelsExampleParser(possible_labels)
        example_parser._parse_examples_model_format(file_name_labeled_examples)
        return example_parser.examples_found


def test():
    test = 'begin(model(2)).'
    test_term = Term.from_string(test)
    print(test_term)

if __name__ == '__main__':
    test()