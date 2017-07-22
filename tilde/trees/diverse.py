from tilde.trees.TreeNode import FOLDecisitionTree

def learn_FOLDT(example_list):
    """Learn a FOLDT using a list of labeled examples"""
    foldt = FOLDecisitionTree()


def is_current_example_set_sufficiently_homogenous(examples):
    """
    Test to decide whether to turn a node into a leaf
    :return:
    """
    return False


# def get_best_refined_query(query, example_list):
#     possible_refined_queries = calculate_possible_refined_queries(query, example_list)
#
#     best_query, best_score = None, 0
#     for query in possible_refined_queries:
#         score = compute_score_for_possible_test_in_node(query, example_list)
#         if score > best_score:
#             best_query = query
#     return best_query



def get_majority_class_of_example_set(query, example_list):
    pass


def compute_score_for_possible_test_in_node():
    """
    TILDE uses the INFORMATION GAIN to determine the best test
    :return:
    """
    pass


def compute_all_possible_tests_in_node():
    """
    This is the most important difference from a traditional propositional tree learner
    --> the generation of tests to be incorporated in the nodes.

    Algorithm in book: employs a refinement operator rho under theta-subsumpion.

    Assumpion in example:
    the refinement operator specializes a query Q, i.e. a set of literals,
    by adding literals l to the query
    yielding the query Q,l

    from the paper:
    rho maps a clause onto a set of clauses,
    such that for any clause c and for all c' in rho(c):
        c theta-subsumes c'
    A clause c1 theta-subsumes another clause c2
        iff
    there is a variable substitution theta
        such that c1 theta is a subset of c2


    :return:
    """
    pass