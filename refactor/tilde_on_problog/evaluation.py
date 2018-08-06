from typing import Optional

import problog
from problog.engine import GenericEngine, DefaultEngine, ClauseDB
from problog.logic import Term, Var
from problog.program import LogicProgram, SimpleProgram, PrologString

from refactor.tilde_essentials.evaluation import TestEvaluator
from tilde.representation.TILDE_query import TILDEQuery


class ProblogQueryEvaluator(TestEvaluator):
    def evaluate(self, instance, test):
        raise NotImplementedError('abstract method')

    def __init__(self, engine: GenericEngine = None):
        if engine is None:
            self.engine = DefaultEngine()
            self.engine.unknown = 1
        else:
            self.engine = engine
        self.to_query = Term('to_query')


class SimpleProgramQueryEvaluator(ProblogQueryEvaluator):
    def __init__(self,
                 background_knowledge: Optional[LogicProgram] = None,
                 engine: GenericEngine = None):
        super().__init__(engine=engine)
        if background_knowledge is None:
            self.db = self.engine.prepare(SimpleProgram())  # type: ClauseDB
        else:
            self.db = self.engine.prepare(background_knowledge)  # type: ClauseDB

        self.db += Term('query')(self.to_query)

    def evaluate(self, instance: SimpleProgram, query: TILDEQuery):

        query_conj = query.to_conjunction()

        db_to_query = self.db.extend()

        for statement in instance:
            db_to_query += statement

        db_to_query += (self.to_query << query_conj)

        query_result = problog.get_evaluatable().create_from(db_to_query, engine=self.engine).evaluate()

        return query_result[self.to_query] > 0.5


if __name__ == '__main__':
    instance = PrologString("""
    color(blue).
    taste(sweet).
    texture(fruity).
    
    """)
    query = TILDEQuery(None, Term('color')(Var('X')))

    evaluator = SimpleProgramQueryEvaluator()

    result = evaluator.evaluate(instance, query)
    print(result)


