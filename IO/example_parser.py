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

from problog.engine import ClauseDB
from problog.program import PrologString
from problog.engine import DefaultEngine

from representation.example import Example

file_name_labeled_examples = 'D:\\KUL\\KUL MAI\\Masterproef\\ACE\\ace\\mach\\examples\\mach.kb'
begin_model_regex = r'begin\(model\((\d+)\)\)\.\n'
end_model_regex = r'end\(model\((\d+)\)\)\.\n'
testnr_regex = r'testnr\('
begin_pattern = re.compile(begin_model_regex)
end_pattern = re.compile(end_model_regex)


class ExampleParseException(Exception):
    pass


def test():
    with open(file_name_labeled_examples, 'r') as f:
        parsing_example = False
        digit = None  # type: Optional(int)

        prolog_string_accumulator = ''

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

                        example = parse_example_string(prolog_string_accumulator)
                        # TODO: do something with the example

                else:
                    prolog_string_accumulator = prolog_string_accumulator + line


# TODO: highly inefficient to do this here
# recompiling the regices of the labels for each example is not good
# also, might be able to check this already while iterating over the lines
def parse_example_string(prolog_string: str, possible_labels: Optional[Iterable[str]] = None) -> Example:
    labeled = (possible_labels is not None)
    if labeled:
        example_labels = set()

        for possible_label in possible_labels:
            label_pattern = re.compile(possible_label)
            # TODO: this might be wrong

            pattern_matched = label_pattern.search(prolog_string + r'\.\n')

            if pattern_matched is not None:
                example_labels.add(possible_label)

        if len(example_labels) == 1:
            label = example_labels.pop()
            prolog_str_without_label = prolog_string.replace(label + '.\n')
            example = PrologString(prolog_str_without_label)
            example.label = label
            return example
    else:
        pass



if __name__ == '__main__':
    test()