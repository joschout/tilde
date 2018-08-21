import os

from mai_experiments.experiment_settings import FileNameData
from refactor.back_end_picking import QueryBackEnd

test_and_logic_names = [
    ('mutab0', 'muta-d'),
    ('mutaace1', 'muta-d'),
    ('financial', 'financial-d-mod'),
    ('canc', 'canc-d'),
    ('bongard4', 'bongard'),
]

back_end_names = [
    QueryBackEnd.SUBTLE.name,
    QueryBackEnd.FLGG.name,
    QueryBackEnd.DJANGO.name
]

data_dict = {}
for back_end_name in back_end_names:
    dict_for_back_end = {}
    for test_name, _ in test_and_logic_names:
        test_dict_for_back_end = {}
        dict_for_back_end[test_name] = test_dict_for_back_end
    data_dict[back_end_name] = dict_for_back_end


def read_files(file_name_data: FileNameData, back_end_name: str, fold_fname_prefix: str,
               test_dict_for_back_end
               ):
    statistics_fname = os.path.join(file_name_data.output_dir,
                                    back_end_name + "_" + fold_fname_prefix + ".statistics")
    with open(statistics_fname, 'r') as ifile:
        for line in ifile:
            splitted_line = line.split(':')
            first_token = splitted_line[0]
            if (first_token == 'mean accuracy' or
                    first_token == 'mean decision tree build time (ms)' or
                    first_token == 'mean fold execution time (ms)' or
                    first_token == 'mean total nb of nodes' or
                    first_token == 'mean nb of inner nodes' or
                    first_token == 'total time cross  (sum folds) (ms)'):
                test_dict_for_back_end[first_token] = splitted_line[1]
