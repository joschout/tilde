# README

This package contains a rework of the [ProbLog](https://dtai.cs.kuleuven.be/problog/)-based TILDE-code. 
The main focus of this rework is separation of the general FOL-decision tree learning code
and the ProbLog code which was used for representing logic, examples, queries ..., and for evaluating the queries on examples.

Separating the high-level decision-tree learning code from ProbLog allows the use of other libraries for representation and evaluation of queries and examples.

The structure of this package is as follows:

* tilde_essentials: This package contains the high-level FOL decision tree learning code.
  The goal is for it to not have any depencencies on the ProbLog library anymore.
* tilde_on_problog: this uses [ProbLog](https://dtai.cs.kuleuven.be/problog/) both for representation and evaluation of examples and queries.
  It should evolve to have the same functionality as was present in the master thesis code.
  At the moment, it only uses SimplePrograms for representing examples; it does not yet support ClauseDBs.
* tilde_on_django: This package uses the [Django](https://tao.lri.fr/tiki-index.php?page=Django) subsumption engine for evaluating queries on examples.
  It uses ProbLog for IO and initial representation of examples and queries.
  These are converted to Python wrappers around the C-based Django structures which are fed into the Django subsumption procedure.
* tilde_on_FLGG: this uses the Java subsumption engine as described by 
  > Fuksová, A. (2007). Fast relational learning using bounded LGG. Journal of Machine Learning Research, 8, 549–587.
  
  It uses ProbLog for IO and initial representation of examples and queries. 
  These are converted to strings in a format that should be accepted by the subsumption engine.
  The subsumption engine should be started as a separate Java process before running this code.
  The communication is done using [Py4J](https://www.py4j.org/).
 
## TILDE essentials package

### Overview
A short overview of the functionality of the high-level FOL decision tree package. 
For more up-to-date info, see the source files.

* evaluation: 
  - abstract TestEvaluator class: used for evaluating a test on an example

* example:
  - Example: Container class for an example, storing its data and label (types undefined)

* leaf_strategy:
  - abstract LeafStrategy class: used in a leaf node for making a prediction for an example
  - MajorityClassLS: predict for an example the majority class of a leaf
  - LeafBuilder: create a leaf strategy based on the training examples (sorted into a leaf node)

* split_criterion:
  - SplitCriterion: Abstract class for calculating a split criterion heuristic 
    using the training examples in a node, split into the subsets of examples satisfying a test and those not satisfying that test.
  - InformationGain: calculates the information gain (for use as a split criterion)
  - SplitCriterionBuilder: Get a split criterion based on its name as a string.

* splitter:
  - Splitter: Finds the best test for splitting a node based on the node's training examples.
    It must be initialized with a SplitCriterion and TestEvaluator.
    Reports the split info using a SplitInfo object
  - SplitInfo: Contains the information about a split using a test on a set of training examples.
  
* stop_criterion:
  - StopCriterion: 
  
* test_generation:
  - abstract TestGeneratorBuilder
  - abstract FOLTestGeneratorBuilder
  
* tree:
  - DecisionTree
  
* tree_builder:

* tree_node:

* tree_printer:

* tree_pruning:

