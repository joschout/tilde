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
from typing import Optional, Iterable

from problog.program import PrologString, LogicProgram


begin_model_regex = r'begin\(model\((\d+)\)\)\.\n'
end_model_regex = r'end\(model\((\d+)\)\)\.\n'
testnr_regex = r'testnr\('
begin_pattern = re.compile(begin_model_regex)
end_pattern = re.compile(end_model_regex)

class ExampleParseException(Exception):
    pass

def parse_examples_model_format(file_name_labeled_examples:str, possible_labels=None) -> Iterable[LogicProgram]:

    examples_found = []

    # getting regex patterns for all possible labels
    label_patterns = []

    if possible_labels is not None:
        for possible_label in possible_labels:
            label_patterns.append((possible_label, re.compile(str(possible_label) + '.\n')))

    with open(file_name_labeled_examples, 'r') as f:
        parsing_example = False
        digit = None  # type: Optional(int)

        prolog_string_accumulator = ''
        example_labels = set()

        for line in f:
            result_of_pattern_matching = None
            if not parsing_example:  # no unclosed parameter delimiters
                result_of_pattern_matching = begin_pattern.search(line)
                # search for the begin(model(digits)). delimiter

                # if we have found the beginning delimiter of an example
                if result_of_pattern_matching is not None:
                    digit = result_of_pattern_matching.group(1)
                    parsing_example = True
                    prolog_string_accumulator = ''
                    example_labels = set()
                else:
                    pass
            else:  # parsing an example, i.e. an open begin(model(digit)). is still unclosed
                result_of_pattern_matching = end_pattern.search(line)
                if result_of_pattern_matching is not None:
                    end_digit = result_of_pattern_matching.group(1)
                    if digit != end_digit:
                        raise ExampleParseException("The example number in the begin and end tags do not match")
                    else:
                        parsing_example = False

                        example = parse_example_string(prolog_string_accumulator, example_labels)
                        # TODO: do something with the example
                        examples_found.append(example)

                else:
                    current_line_is_label = False
                    matches_label = None
                    for label, label_pattern in label_patterns:
                        matches_label = label_pattern.search(line)
                        if matches_label is not None:
                            example_labels.add(label)
                            current_line_is_label = True
                    if current_line_is_label is False:
                        prolog_string_accumulator = prolog_string_accumulator + line
    return examples_found


def parse_example_string(prolog_string_unlabeled: str, example_labels=None) -> LogicProgram:

    example = PrologString(prolog_string_unlabeled)
    if example_labels is not None:
         if len(example_labels) == 1:
            example.label = example_labels.pop()
         else:
            example.label = example_labels
    return example
