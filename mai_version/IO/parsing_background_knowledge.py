from typing import Optional, Iterable, List

from problog.logic import Term
from problog.program import PrologFile, SimpleProgram

from mai_version.representation.background_knowledge import BackgroundKnowledgeWrapper


#
def parse_background_knowledge(file_name: str)-> PrologFile:
    return PrologFile(file_name)


def parse_background_knowledge_models(file_name: Optional[str] = None,
                                      possible_labels: Optional[Iterable[Term]] = None) -> BackgroundKnowledgeWrapper:
    if file_name is None:
        return BackgroundKnowledgeWrapper()

    logic_program = PrologFile(file_name)

    if possible_labels is not None:
        possible_labels_str = [str(label) for label in possible_labels]  # type: List[str]

        found_a_prediction_clause = False

        prediction_goal_clauses = SimpleProgram()
        stripped_logic_program = SimpleProgram()

        for prolog_statement in logic_program:
            is_prediction_clause = False
            for possible_label_str in possible_labels_str:
                if str(prolog_statement).startswith(possible_label_str):
                    is_prediction_clause = True
                    found_a_prediction_clause = True
                    break

            if is_prediction_clause:
                prediction_goal_clauses += prolog_statement
            else:
                stripped_logic_program += prolog_statement

        if found_a_prediction_clause:
            return BackgroundKnowledgeWrapper(logic_program=stripped_logic_program,
                                              prediction_goal_clauses=prediction_goal_clauses)
        else:
            return BackgroundKnowledgeWrapper(logic_program=logic_program)
    else:
        return BackgroundKnowledgeWrapper(logic_program=logic_program)


def parse_background_knowledge_keys(file_name: Optional[str] = None,
                                    prediction_goal: Optional[Term] = None) -> BackgroundKnowledgeWrapper:
    if file_name is None:
        return BackgroundKnowledgeWrapper()

    logic_program = PrologFile(file_name)

    if prediction_goal is not None:
        prediction_goal_functor = prediction_goal.functor  # type: str

        found_a_prediction_goal_clause = False

        prediction_goal_clauses = SimpleProgram()
        stripped_logic_program = SimpleProgram()

        for prolog_statement in logic_program:
            if str(prolog_statement).startswith(prediction_goal_functor):
                found_a_prediction_goal_clause = True
                prediction_goal_clauses += prolog_statement
            else:
                stripped_logic_program += prolog_statement

        if found_a_prediction_goal_clause:
            return BackgroundKnowledgeWrapper(logic_program=stripped_logic_program,
                                              prediction_goal_clauses=prediction_goal_clauses)
        else:
            return BackgroundKnowledgeWrapper(logic_program=logic_program)
    else:
        return BackgroundKnowledgeWrapper(logic_program=logic_program)
