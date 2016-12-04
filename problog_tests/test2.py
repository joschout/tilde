from problog.logic import *
from problog.program import SimpleProgram
from problog.engine import DefaultEngine

# defining the terms
sendback, fix, ok, worn, replaceable = \
    Term('sendback'), Term('fix'), Term('ok'), Term('worn'), Term('replaceable')
p0, p1, class_ = \
    Term('p0'), Term('p1'), Term('class')

# defining the constants
gear, engine, chain = \
    Constant('gear'), Constant('engine'), Constant('chain')

X = Var('X')

def main():
    ex1 = SimpleProgram()

    ex1 += worn(gear)
    ex1 += worn(engine)
    ex1 += replaceable(gear)

    rules = SimpleProgram()
    rules += (p0 << worn(X))
    rules += (p1 << (worn(X) & ~replaceable(X)))
    rules += (sendback << (worn(X) & ~replaceable(X)))
    rules += (fix << (worn(X) & ~p1))
    rules += (ok << ~p0)

    eng = DefaultEngine()
    db = eng.prepare(ex1)
    db2 = db.extend()  # creates a new db2 with as its parent db

    for statement in rules:
        db2 += statement

    query_term = sendback

    result_sendback = eng.query(db2, query_term)
    print('example 1: Sendback: ' + str(bool(result_sendback))
          + ', fix: ' + str(bool(eng.query(db2, fix)))
          + ', ok: ' + str(bool(eng.query(db2, ok))))

    print(getLabel([ex1], rules))


def getLabel(example_list, rules):
    label_list = []
    for example in example_list:
        eng = DefaultEngine()
        eng.unknown = 1
        db = eng.prepare(example)
        for rule in rules:
            db += rule
        result_list = [eng.query(db, x) for x in [sendback, fix, ok]]
        label_list_str = [str(bool(result)) for result in result_list]
        labels_str = 'sendback: ' + label_list_str[0] + ', fix: ' + label_list_str[1] + ', ok: ' + label_list_str[2]
        label_list.append(labels_str)
    return label_list
if __name__ == '__main__':
    main()
