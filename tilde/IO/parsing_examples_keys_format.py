from typing import Dict, List, Optional

from problog.logic import Term
from problog.program import PrologFile

from tilde.representation.example import SimpleProgramExampleWrapper


# def parse_examples_key_format_without_key(file_name_labeled_examples: str) -> List[SimpleProgramExample]:
#     examples_found = {}  # type: Dict[Term, SimpleProgramExample]
#
#     file = PrologFile(file_name_labeled_examples)  # type: PrologFile
#     for prolog_statement in file:  # type: Term
#         example_key = prolog_statement.args[0]  # type: Term
#         prolog_statement_without_key = prolog_statement(*prolog_statement.args[1:])
#         if example_key not in examples_found:
#             new_example = SimpleProgramExample()
#             new_example.key = example_key  # type: Term
#             new_example += prolog_statement_without_key
#             examples_found[example_key] = new_example
#         else:
#             examples_found[example_key] += prolog_statement_without_key
#     return list(examples_found.values())


# def parse_examples_key_format_with_key(file_name_labeled_examples: str) -> List[SimpleProgramExample]:
#     examples_found = {}  # type: Dict[Term, SimpleProgramExample]
#
#     file = PrologFile(file_name_labeled_examples)  # type: PrologFile
#     for prolog_statement in file:  # type: Term
#         example_key = prolog_statement.args[0]
#         if example_key not in examples_found:
#             new_example = SimpleProgramExample()
#             new_example.key = example_key  # type: Term
#             new_example += prolog_statement
#             examples_found[example_key] = new_example
#         else:
#             examples_found[example_key] += prolog_statement
#     return list(examples_found.values())


def parse_examples_key_format_with_key(file_name_labeled_examples: str, prediction_goal: Optional[Term]=None) -> List[SimpleProgramExampleWrapper]:

    prediction_goal_functor = prediction_goal.functor

    examples_found = {}  # type: Dict[Term, SimpleProgramExampleWrapper]

    file = PrologFile(file_name_labeled_examples)  # type: PrologFile

    for prolog_statement in file:  # type: Term
        example_key = prolog_statement.args[0]
        if example_key not in examples_found:
            new_example = SimpleProgramExampleWrapper()
            new_example.key = example_key  # type: Term

            if prolog_statement.functor.startswith(prediction_goal_functor):
                new_example.classification_term = prolog_statement
            else:
                new_example += prolog_statement
            examples_found[example_key] = new_example
        else:
            if prolog_statement.functor.startswith(prediction_goal_functor):
                examples_found[example_key].classification_term = prolog_statement
            else:
                examples_found[example_key] += prolog_statement

    return list(examples_found.values())
