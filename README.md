# TILDE: top-down induction of first-order logical  decision trees 

This repository contains an implementation of the TILDE algorithm for classification. 
The implementation is in function of my master thesis in Artificial Intelligence.
The TILDE algorithm was proposed in:
> Blockeel, H., & De Raedt, L. (1998). Top-down induction of first-order logical decision trees. Artificial Intelligence, 101(1�2), 285�297. http://doi.org/10.1016/S0004-3702(98)00034-4

This repository contains two versions:
* The [mai_version](mai_version/) package contains the version made for my master thesis.

* The [refactor](refactor/) package contains a rewrite of the core functionality. 
The goal of the rewrite was to reduce the dependency on *ProbLog* for query and example representations.
Different query engines can now be used as a back end for testing queries on examples, such as Django, FLGG and Subtle.
Other query engines can be added easily by implementing a wrapper with the required interface.
The *refactor* package contains its own [README.md](refactor/README.md) file introducing the package's content. 
Currently, it still uses some functionality from the *mai_version* package, for example for IO. 
This might be removed in a future refactor, as this could also be abstracted away from ProbLog.

## How do I get set up?

Pyhon 3.6 or higher is required, since the typing module is used.

When using Django, you should have a compiled version of the Django subsumption engine.


## Example data sets

A couple of toy example data sets to get started with
 can be found in [the ACE documentation](https://dtai.cs.kuleuven.be/ACE/doc/).
 
 
## A refactored TILDE version

This [refactor](refactor/) contains a rework of the [ProbLog](https://dtai.cs.kuleuven.be/problog/)-based TILDE-code. 
The main focus of this rework is separation of the general FOL-decision tree learning code
and the ProbLog code which was used for representing logic, examples, queries ..., and for evaluating the queries on examples.

Separating the high-level decision-tree learning code from ProbLog allows the use of other libraries for representation and evaluation of queries and examples.

The structure of this package is as follows:

* tilde_essentials: This package contains the high-level FOL decision tree learning code.
  The goal is for it to not have any depencencies on the ProbLog library anymore.
* query_testing_back_end: different implementations of the interfaces to test queries on examples 
    * problog: this uses [ProbLog](https://dtai.cs.kuleuven.be/problog/) both for representation and evaluation of examples and queries.
      It should evolve to have the same functionality as was present in the master thesis code.
      At the moment, it only uses SimplePrograms for representing examples; it does not yet support ClauseDBs.
    * django: This package uses the [Django](https://tao.lri.fr/tiki-index.php?page=Django) subsumption engine for evaluating queries on examples.
      It uses ProbLog for IO and initial representation of examples and queries.
      These are converted to Python wrappers around the C-based Django structures which are fed into the Django subsumption procedure.
    * flgg_py4j: this uses the Java subsumption engine as described by 
      > Fuksov�, A. (2007). Fast relational learning using bounded LGG. Journal of Machine Learning Research, 8, 549�587. 
      
        It uses ProbLog for IO and initial representation of examples and queries. 
        These are converted to strings in a format that should be accepted by the subsumption engine.
        The subsumption engine should be started as a separate Java process before running this code.
        The communication is done using [Py4J](https://www.py4j.org/).
    * subtle: This package uses the [Subtle](https://dtai.cs.kuleuven.be/software/subtle/) subsumption engine. It requires SWI-Prolog to be installed. 
      The communication with SWI-Prolog is done using [PySwip](https://github.com/yuce/pyswip).
      From Python, SWI-Prolog is called as a library, in which the Subtle engine is consulted. 

### TILDE essentials package

#### Overview
A short overview of the functionality of the high-level FOL decision tree package. 
For more up-to-date info, see the source files.

* evaluation: 
    - TestEvaluator (abstract class): used for evaluating a test on an example

* example:
    - Example: Container class for an example, storing its data and label (types undefined)

* leaf_strategy:
    - LeafStrategy (abstract class): used in a leaf node for making a prediction for an example
    - MajorityClassLS: predict for an example the majority class of a leaf
    - LeafBuilder: create a leaf strategy based on the training examples (sorted into a leaf node)

* split_criterion:
    - SplitCriterion (abstract class): Calculates a split criterion heuristic 
      using the training examples in a node, split into the subsets of examples satisfying a test and those not satisfying that test.
    - InformationGain: calculates the information gain (for use as a split criterion)
    - SplitCriterionBuilder: Get a split criterion based on its name as a string.

* splitter:
    - Splitter: Finds the best test for splitting a node based on the node's training examples.
        It must be initialized with a SplitCriterion and TestEvaluator.
        Reports the split info using a SplitInfo object
    - SplitInfo: Contains the information about a split using a test on a set of training examples.
  
* stop_criterion:
    - StopCriterion: Checks whether a the node should be split; i.e. whether a stop criterion is reached.
  
* test_generation:
    - TestGeneratorBuilder (abstract class): Builds a generator to produce possible tests in a node to be split.
    - FOLTestGeneratorBuilder (abstract class): Builds a generator to produce possible tests in a node to be split.
        Finds the associated test of the node, which is the test of the ancestor of the current node whose test should be refined. 
  
* tree:
    - DecisionTree: Decision tree used for making predictions. Initially empty. 
        An internal TreeNode tree is fitted on training examples using a TreeBuilder.
  
* tree_builder:
    - TreeBuilder: Builds a TreeNode tree in a top-down fashion by recursively splitting nodes.
        Uses:
        - a Splitter to determine the best split of a node
        - a LeafBuilder to determine the leaf prediction strategy of leaf nodes
        - a StopCriterion to halt the recursion

* tree_node:
    - TreeNode: Binary tree data structure. Should have 0 or 2 child nodes.
    - TreeNodePrinter: Pretty prints a TreeNode tree structure.

* tree_pruning:
    - abstract TreePruner: Prunes a TreeNode tree structure.

#### Usage

```python
from refactor.tilde_essentials.example import Example
from refactor.tilde_essentials.leaf_strategy import LeafBuilder
from refactor.tilde_essentials.splitter import Splitter
from refactor.tilde_essentials.stop_criterion import StopCriterion
from refactor.tilde_essentials.tree import DecisionTree
from refactor.tilde_essentials.tree_builder import TreeBuilder
from refactor.tilde_on_problog.evaluation import SimpleProgramQueryEvaluator
from refactor.tilde_on_problog.test_generation import ProbLogTestGeneratorBuilder

from problog.logic import Term, Var, Constant

# NOTE: include a non-empty example list
language = ...
examples = ...  # type: List[Example]
prediction_goal = Term('bongard')(Var('A',Constant('pos')))
engine = ... # ProbLog engine

test_evaluator = SimpleProgramQueryEvaluator()

test_generator_builder = ProbLogTestGeneratorBuilder(language=language,
                                                     query_head_if_keys_format=prediction_goal)
splitter = Splitter(split_criterion_str='entropy', test_evaluator=test_evaluator,
                    test_generator_builder=test_generator_builder)
leaf_builder = LeafBuilder()
stop_criterion = StopCriterion()
tree_builder = TreeBuilder(splitter=splitter, leaf_builder=leaf_builder, stop_criterion=stop_criterion)
decision_tree = DecisionTree()


decision_tree.fit(examples=examples, tree_builder=tree_builder)

print(decision_tree)

```
