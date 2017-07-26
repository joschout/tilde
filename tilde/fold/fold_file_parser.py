import os
from typing import Set, List

from tilde.IO.parsing_background_knowledge import parse_background_knowledge
from tilde.IO.parsing_settings.setting_parser import SettingsParserMapper
from tilde.IO.parsing_settings.utils import ConstantBuilder
from tilde.main import ProgramSettings, kb_suffix, s_suffix, bg_suffix
from tilde.representation.example import Example
from tilde.run.program_phase import preprocessing_examples_keys, build_tree, convert_tree_to_program


def learn_model(training_examples):
    pass


def evaluate_model(test_examples):
    pass


def parse(fprefix, settings: ProgramSettings):
    list_of_files = os.listdir(os.getcwd())

    prefixed_fnames = [fname for fname in list_of_files if fname.startswith(fprefix)]

    if len(prefixed_fnames) <= 1:
        raise Exception("more than 1 fold file is needed")

    fname_labeled_examples = settings.filename_prefix + kb_suffix
    fname_settings = settings.filename_prefix + s_suffix

    # BACKGROUND KNOWLEDGE
    if settings.use_bg:
        fname_background_knowledge = settings.filename_prefix + bg_suffix
        background_knowledge = parse_background_knowledge(fname_background_knowledge)
    else:
        background_knowledge = None

    debug_printing = settings.debug_parsing

    settings_file_parser = SettingsParserMapper.get_settings_parser(settings.kb_format)
    parsed_settings = settings_file_parser.parse(fname_settings)
    examples, prediction_goal, index_of_label_var, possible_labels = \
        preprocessing_examples_keys(fname_labeled_examples, parsed_settings, settings.internal_examples_format,
                                    background_knowledge)

    # read in all the keysets
    key_sets = []  # type: List[Set[Example]]
    for fname in prefixed_fnames:
        key_sets.append(get_keys_in_fold_file(fname))

    # take one key set as test, the others as training
    for index, test_set_keys in enumerate(key_sets):
        sets = [s for s in key_sets if s is not test_set_keys]

        training_set_keys = set.union(*sets)
        training_examples = filter_examples(examples, training_set_keys)
        test_examples = filter_examples(examples, test_set_keys)


        # TRAIN MODEL using training set
        tree = build_tree(settings.internal_examples_format, settings.treebuilder_type, parsed_settings.language,
                          possible_labels, training_examples, prediction_goal=prediction_goal,
                          background_knowledge=background_knowledge,
                          debug_printing=debug_printing)

        program = convert_tree_to_program(settings.kb_format, settings.treebuilder_type, tree, parsed_settings.language,
                                          debug_printing=debug_printing, prediction_goal=prediction_goal,
                                          index_of_label_var=index_of_label_var)

        # EVALUATE MODEL using test set


        # train using training set
        learn_model(training_examples)

        # evaluate tree using test set\
        evaluate_model(test_examples)


def filter_examples(examples: List[Example], key_set: Set[Example]):
    return [ex for ex in examples if ex.key in key_set]


def get_keys_in_fold_file(fname: str):
    key_set = set()

    with open(fname, 'r') as f:
        for line in f:
            split_line = line.split(':')
            key = split_line[0]
            key_set.add(ConstantBuilder.parse_constant_str(key))
    return key_set


def main():
    fname_prefix = 'data//test'
    parse(fname_prefix)



if __name__ == '__main__':
    main()
