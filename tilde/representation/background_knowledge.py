from typing import Optional

from problog.engine import DefaultEngine, ClauseDB
from problog.logic import Term
from problog.program import SimpleProgram, PrologFile


class BackgroundKnowledgeWrapper:
    def __init__(self, logic_program=None, prediction_goal_clauses=None, full_logic_program = None):
        """
        argument full_logic_program might be used if the ORDER of facts is important in the full background knowledge?

        :param logic_program:
        :param prediction_goal_clauses:
        :param full_logic_program:
        """
        self.logic_program = logic_program  # type: Optional[SimpleProgram]
        self.prediction_goals_clauses = prediction_goal_clauses  # type: Optional[SimpleProgram]

        self.full_background_knowledge_clausedb = None  # type: Optional[ClauseDB]
        self.stripped_background_knowledge_clausedb= None  # type: Optional[ClauseDB]

    def get_stripped_background_knowledge(self) -> Optional[SimpleProgram]:
        return self.logic_program

    def has_prediction_goal_clauses(self) -> bool:
        return self.prediction_goals_clauses is not None

    def has_background_knowledge(self):
        return self.logic_program is not None or self.prediction_goals_clauses is not None

    def get_full_background_knowledge_simple_program(self) -> Optional[SimpleProgram]:
        if not self.has_background_knowledge():
            return None

        elif self.logic_program is not None and self.prediction_goals_clauses is not None:
            full_bg_kw = SimpleProgram()

            for lp_statement in self.logic_program:
                full_bg_kw += lp_statement

            for pgc_statement in self.prediction_goals_clauses:
                full_bg_kw += pgc_statement

            return full_bg_kw

        elif self.logic_program is not None:
            return self.logic_program
        else:
            return self.prediction_goals_clauses

    def get_full_background_knowledge_clausedb(self) -> ClauseDB:
        if self.full_background_knowledge_clausedb is not None:
            return self.full_background_knowledge_clausedb
        else:
            engine = DefaultEngine()
            engine.unknown = 1

            full_bg_kw = self.get_full_background_knowledge_simple_program()

            if full_bg_kw is not None:
                self.full_background_knowledge_clausedb = engine.prepare(full_bg_kw)  # ClauseDB
                return self.full_background_knowledge_clausedb
            else:
                raise Exception("No sense in making an empty ClauseDB for an empty background knowledge")


    # @staticmethod
    # def parse_background_knowledge_experimental(file_name: Optional[str] = None,
    #                                             prediction_goal: Optional[Term] = None) -> 'BackgroundKnowledgeWrapper':
    #     if file_name is None:
    #         return BackgroundKnowledgeWrapper()
    #
    #     logic_program = PrologFile(file_name)
    #
    #     if prediction_goal is not None:
    #         prediction_goal_functor = prediction_goal.functor  # type: str
    #
    #         found_a_prediction_goal_clause = False
    #
    #         prediction_goal_clauses = SimpleProgram()
    #         stripped_logic_program = SimpleProgram()
    #
    #         for prolog_statement in logic_program:
    #             if prolog_statement.functor.startswith(prediction_goal_functor):
    #                 found_a_prediction_goal_clause = True
    #                 prediction_goal_clauses += prolog_statement
    #             else:
    #                 stripped_logic_program += prolog_statement
    #
    #         if found_a_prediction_goal_clause:
    #             return BackgroundKnowledgeWrapper(logic_program=stripped_logic_program,
    #                                               prediction_goal_clauses=prediction_goal_clauses)
    #         else:
    #             return BackgroundKnowledgeWrapper(logic_program=logic_program)
    #     else:
    #         return BackgroundKnowledgeWrapper(logic_program=logic_program)
