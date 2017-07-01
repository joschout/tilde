def print_partition_subset_sizes(examples_satisfying_best_query, examples_not_satisfying_best_query):
    print('# examples satisfying best query: ', len(examples_satisfying_best_query))
    if examples_satisfying_best_query is not None:
        label_counts_sat = {}
        for example in examples_satisfying_best_query:
            if example.label in label_counts_sat:
                label_counts_sat[example.label] += 1
            else:
                label_counts_sat[example.label] = 1
        print('\tlabel counts:' + str(label_counts_sat))

    print('# examples not satisfying best query: ', len(examples_not_satisfying_best_query))
    if examples_not_satisfying_best_query is not None:
        label_counts_not_sat = {}
        for example in examples_not_satisfying_best_query:
            if example.label in label_counts_not_sat:
                label_counts_not_sat[example.label] += 1
            else:
                label_counts_not_sat[example.label] = 1
        print('\tlabel counts:' + str(label_counts_not_sat))
