# README

This module contains a rework of the [ProbLog](https://dtai.cs.kuleuven.be/problog/)-based TILDE-code. 
The main focus of this rework is separation of the general FOL-decision tree learning code
and the ProbLog code which was used for representing logic, examples, queries ..., and for evaluating the queries on examples.

Separating the high-level decision-tree learning code from ProbLog allows the use of other libraries for representation and evaluation of queries and examples.

The structure of this module is as follows:

* tilde_essentials: This module contains the high-level FOL decision tree learning code.
  The goal is for it to not have any depencencies on the ProbLog library anymore.
* tilde_on_problog: this uses [ProbLog](https://dtai.cs.kuleuven.be/problog/) both for representation and evaluation of examples and queries.
  It should evolve to have the same functionality as was present in the master thesis code.
  At the moment, it only uses SimplePrograms for representing examples; it does not yet support ClauseDBs.
* tilde_on_django: This module uses the [Django](https://tao.lri.fr/tiki-index.php?page=Django) subsumption engine for evaluating queries on examples.
  It uses ProbLog for IO and initial representation of examples and queries.
  These are converted to Python wrappers around the C-based Django structures which are fed into the Django subsumption procedure.
* tilde_on_FLGG: this uses the Java subsumption engine as described by 
  > Fuksová, A. (2007). Fast relational learning using bounded LGG. Journal of Machine Learning Research, 8, 549–587.
  
  It uses ProbLog for IO and initial representation of examples and queries. 
  These are converted to strings in a format that should be accepted by the subsumption engine.
  The subsumption engine should be started as a separate Java process before running this code.
  The communication is done using [Py4J](https://www.py4j.org/).
 

