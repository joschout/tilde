from typing import Dict, List

from classification.classification_helper import Label
from problog.engine import DefaultEngine
from problog.program import PrologString, PrologFile
from representation.example import Example, Probability
from representation.language import TypeModeLanguage

from tilde.IO.parsing_examples_models_format import ModelsExampleParser
from tilde.IO.parsing_settings import SettingParser, Settings
from tilde.IO.parsing_background_knowledge import parse_background_knowledge
from tilde.classification.classification import get_labels_single_example_probabilistic_models

ESTIMATION_ERROR = 0.01

fname_settings = 'D:\\KUL\\KUL MAI\\Masterproef\\ACE\\ace\\mach\\examples-experimental\\mach.s'
fname_background_knowledge = 'D:\\KUL\\KUL MAI\\Masterproef\\ACE\\ace\\mach\\examples-experimental\\mach.bg'
fname_labeled_examples = 'D:\\KUL\\KUL MAI\\Masterproef\\ACE\\ace\\mach\\examples-experimental\\mach.kb'

# fname_settings = 'D:\\KUL\\KUL MAI\\Masterproef\\ACE\\ace\\mach\\examples\\mach.s'
# fname_background_knowledge = 'D:\\KUL\\KUL MAI\\Masterproef\\ACE\\ace\\mach\\examples\\mach.bg'
# fname_labeled_examples = 'D:\\KUL\\KUL MAI\\Masterproef\\ACE\\ace\\mach\\examples\\mach.kb'

program = PrologString(
"""pred0 :- worn(A).
pred1 :- worn(A), not_replaceable(A).
sendback :- worn(A), not_replaceable(A).
fix :- worn(A), \+pred1.
ok :- \+pred0.
""")

engine = DefaultEngine()
engine.unknown = 1

# SETINGS for MODELS format
settings = SettingParser.get_settings_models_format(fname_settings)  # type: Settings
language = settings.language  # type: TypeModeLanguage

# LABELS
possible_targets = settings.possible_labels  # type: List[Label]

# BACKGROUND KNOWLEDGE
if fname_background_knowledge is not None:
    background_knowledge = parse_background_knowledge(fname_background_knowledge)  # type: PrologFile
else:
    background_knowledge = None

# EXAMPLES
examples = ModelsExampleParser.parse(fname_labeled_examples, possible_targets)

# ====================

nb_of_examples = len(examples)
nb_of_correcty_labeled_examples = 0
nb_of_incorrecty_labeled_examples = 0


nb_of_times_predicted_probability_correct = {}
nb_of_times_predicted_probability_incorrect = {}
for label in possible_targets:
    nb_of_times_predicted_probability_correct[label] = 0
    nb_of_times_predicted_probability_incorrect[label] = 0


for nb, example in enumerate(examples):  # type: Example
    print("example number: " + str(nb + 1))
    true_example_labels = example.get_label_dict()  # type: Dict[Label, Probability]
    query_results =\
        get_labels_single_example_probabilistic_models(example, program, possible_targets, background_knowledge)
    print("Query results:")
    print(query_results)


    for label in possible_targets:
        true_probability_of_label = true_example_labels[label].value  # type: float
        estimated_probability_of_label = query_results[label]  # type: float
        difference = abs(true_probability_of_label - estimated_probability_of_label)
        print("label: " + str(label))
        print("\ttrue:      " + str(true_probability_of_label))
        print("\tpredicted: " + str(estimated_probability_of_label))

        correct_prediction_for_label = difference < ESTIMATION_ERROR
        if correct_prediction_for_label:
            nb_of_times_predicted_probability_correct[label] = nb_of_times_predicted_probability_correct[label] + 1
        else:
            nb_of_times_predicted_probability_incorrect[label] = nb_of_times_predicted_probability_incorrect[label] + 1
            print('\tnoticeable difference in label probabilities')

    true_label_with_max_probability = max(true_example_labels, key=(lambda key: true_example_labels[key].value))
    true_max_probability = true_example_labels[true_label_with_max_probability]
    print("true max label: " + str(true_label_with_max_probability) + " (prob: " + str(true_max_probability) + ")")

    estimated_label_with_max_prob = max(query_results, key=(lambda key: query_results[key]))
    estimated_prob = query_results[estimated_label_with_max_prob]
    print("estimated max label: " + str(estimated_label_with_max_prob) + " (prob: " + str(estimated_prob) + ")")

    if true_label_with_max_probability == estimated_label_with_max_prob:
        print("correctly classified")
        nb_of_correcty_labeled_examples += 1
    else:
        print("NOT correctly classified")
        nb_of_incorrecty_labeled_examples += 1

    print("=============")

print('STATISTICS FOR NERDS')


max_label_str_len = max([len(str(label)) for label in possible_targets])
indent = " " * max_label_str_len
print(indent + "\tnb correct \t nb incorrect")
for label in possible_targets:
    indent_label = " " * (max_label_str_len - len(str(label)))

    print(str(label) + indent_label + "\t" + str(nb_of_times_predicted_probability_correct[label]) + "\t" + str(nb_of_times_predicted_probability_incorrect[label]))

print("total nb of examples: " + str(nb_of_examples))
print(
    "examples labeled correctly: " + str(nb_of_correcty_labeled_examples) + "/" + str(nb_of_examples) + ", " + str(
        nb_of_correcty_labeled_examples / nb_of_examples * 100) + "%")
print("examples labeled incorrectly: " + str(nb_of_incorrecty_labeled_examples) + "/" + str(
    nb_of_examples) + ", " + str(
    nb_of_incorrecty_labeled_examples / nb_of_examples * 100) + "%")

