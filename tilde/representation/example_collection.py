import warnings
from typing import List, Optional, Set

from problog.logic import Constant

from tilde.representation.example import SimpleProgramExampleWrapper, ClauseDBExampleWrapper, ExampleWrapper


class UnlabeledExampleException(Exception):
    pass


class EmptyExampleCollectionException(Exception):
    pass


class ExampleCollection:
    def __init__(self):
        self.example_wrappers_sp = None  # type: Optional[List[SimpleProgramExampleWrapper]]
        self.example_wrappers_clausedb = None  # type: Optional[List[ClauseDBExampleWrapper]]

        self.are_sp_examples_labeled = False  # type: bool
        self.are_clausedb_examples_labeled = False  # type: bool

    def get_example_wrappers_sp(self) -> List[SimpleProgramExampleWrapper]:
        if self.example_wrappers_sp is None:
            raise EmptyExampleCollectionException("There are no SimpleProgram examples")

        if not self.are_sp_examples_labeled:
            warnings.warn("The SimpleProgram examples are not labeled")
        return self.example_wrappers_sp

    def get_example_wrappers_clausedb(self) -> List[ClauseDBExampleWrapper]:
        if self.example_wrappers_clausedb is None:
            raise EmptyExampleCollectionException("There are no ClauseDB examples")

        if not self.are_clausedb_examples_labeled:
            warnings.warn("The ClauseDB examples are not labeled")
        return self.example_wrappers_clausedb

    def get_labeled_example_wrappers_sp(self) -> List[SimpleProgramExampleWrapper]:
        if self.example_wrappers_sp is None:
            raise EmptyExampleCollectionException("There are no SimpleProgram examples")

        # if they are labeled:
        if self.are_sp_examples_labeled:
            return self.example_wrappers_sp
        else: # SimpleProgram examples are not labeled
            if self.are_clausedb_examples_labeled:
                if len(self.example_wrappers_sp) == len(self.example_wrappers_clausedb):
                    # give the label of the clausedb to the corresponding simpleprogram
                    for i in range(0, len(self.example_wrappers_sp)):
                        self.example_wrappers_sp[i].label = self.example_wrappers_clausedb[i].label

                    # set flag: now they are labeled
                    self.are_sp_examples_labeled = True

                    return self.example_wrappers_sp
            else:  # both clausedb and simpleprograms not labeled
                raise UnlabeledExampleException("Both the ClauseDB and SimpleProgram examples are unlabeled")

    def get_labeled_example_wrappers_clausedb(self) -> List[ClauseDBExampleWrapper]:
        if self.example_wrappers_clausedb is None:
            raise EmptyExampleCollectionException("There are no ClauseDB examples")

        if self.are_clausedb_examples_labeled:
            return self.example_wrappers_clausedb
        else:  # clausedb not labeled
            if self.are_sp_examples_labeled:
                if len(self.example_wrappers_sp) == len(self.example_wrappers_clausedb):
                    # give the label of the simpleprogram to the corresponding clausedb
                    for i in range(0, len(self.example_wrappers_sp)):
                        self.example_wrappers_clausedb[i].label = self.example_wrappers_sp[i].label

                    # now the clausedb are labeled!
                    self.are_clausedb_examples_labeled = True

                    return self.example_wrappers_clausedb

            else:  # both clausedb and simpleprograms not labeled
                raise UnlabeledExampleException("Both the ClauseDB and SimpleProgram examples are unlabeled")

    def set_example_wrappers_sp(self, example_wrappers_sp: List[SimpleProgramExampleWrapper]):
        self.example_wrappers_sp = example_wrappers_sp

        # if the examples are labeled, set flag
        if example_wrappers_sp[0].label is not None:
            self.are_sp_examples_labeled = True

    def set_example_wrappers_clausedb(self, example_wrappers_clausedb: List[ClauseDBExampleWrapper]):
        self.example_wrappers_clausedb = example_wrappers_clausedb

        # if the examples are labeled, set flag
        if example_wrappers_clausedb[0].label is not None:
            self.are_clausedb_examples_labeled = True

    def get_examples(self) -> List[ExampleWrapper]:
        if self.example_wrappers_clausedb is not None:
            return self.get_example_wrappers_clausedb()
        if self.example_wrappers_sp is not None:
            return self.get_example_wrappers_sp()
        raise EmptyExampleCollectionException("The collection contains no SimpleProgram and no ClauseDB examples")

    def get_labeled_examples(self) -> List[ExampleWrapper]:
        if self.example_wrappers_clausedb is not None:
            return self.get_labeled_example_wrappers_clausedb()
        if self.example_wrappers_sp is not None:
            return self.get_labeled_example_wrappers_sp()
        raise EmptyExampleCollectionException("The collection contains no SimpleProgram and no ClauseDB examples")

    def filter_examples(self, key_set: Set[Constant]) -> 'ExampleCollection':
        """
        Only KEEPS the examples IN the key_set
        :param key_set:
        :return:
        """
        filtered_collection = ExampleCollection()

        example_wrappers_sp = self.example_wrappers_sp
        example_wrappers_clausedb = self.example_wrappers_clausedb

        if example_wrappers_sp is not None and example_wrappers_clausedb is not None:
            filtered_sp = []
            filtered_clausedb = []

            for ex_index, ex_sp in enumerate(example_wrappers_sp):
                if ex_sp.key in key_set:
                    filtered_sp.append(ex_sp)
                    filtered_clausedb.append(example_wrappers_clausedb[ex_index])
            filtered_collection.set_example_wrappers_sp(filtered_sp)
            filtered_collection.set_example_wrappers_clausedb(filtered_clausedb)
            return filtered_collection

        elif example_wrappers_sp is not None:
            filtered_sp = [ex_sp for ex_sp in example_wrappers_sp if ex_sp.key in key_set]

            filtered_collection.set_example_wrappers_sp(filtered_sp)
            return filtered_collection
        elif example_wrappers_clausedb is not None:
            filtered_clausedb = [ex_clausedb for ex_clausedb in example_wrappers_clausedb if ex_clausedb.key in key_set]

            filtered_collection.set_example_wrappers_clausedb(filtered_clausedb)
            return filtered_collection

        return filtered_collection

    # TODO: merge with function above, they only differ in boolean check
    def filter_examples_not_in_key_set(self, key_set: Set[Constant]) -> 'ExampleCollection':
        """

        Only KEEPS the examples IN the key_set
        :param key_set:
        :return:
        """
        filtered_collection = ExampleCollection()

        example_wrappers_sp = self.example_wrappers_sp
        example_wrappers_clausedb = self.example_wrappers_clausedb

        if example_wrappers_sp is not None and example_wrappers_clausedb is not None:
            filtered_sp = []
            filtered_clausedb = []

            for ex_index, ex_sp in enumerate(example_wrappers_sp):
                if ex_sp.key not in key_set:
                    filtered_sp.append(ex_sp)
                    filtered_clausedb.append(example_wrappers_clausedb[ex_index])
            filtered_collection.set_example_wrappers_sp(filtered_sp)
            filtered_collection.set_example_wrappers_clausedb(filtered_clausedb)
            return filtered_collection

        elif example_wrappers_sp is not None:
            filtered_sp = [ex_sp for ex_sp in example_wrappers_sp if ex_sp.key not in key_set]

            filtered_collection.set_example_wrappers_sp(filtered_sp)
            return filtered_collection
        elif example_wrappers_clausedb is not None:
            filtered_clausedb = [ex_clausedb for ex_clausedb in example_wrappers_clausedb if ex_clausedb.key not in key_set]

            filtered_collection.set_example_wrappers_clausedb(filtered_clausedb)
            return filtered_collection

        return filtered_collection
