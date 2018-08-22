# TILDE: top-down induction of first-order logical  decision trees #

This repository contains an implementation of the TILDE algorithm. The implementation is in function of my master thesis in Artificial Intelligence. An explanation of TILDE can be found in:
> Blockeel, H., & De Raedt, L. (1998). Top-down induction of first-order logical decision trees. Artificial Intelligence, 101(1�2), 285�297. http://doi.org/10.1016/S0004-3702(98)00034-4

The *mai_version* package contains the version made for a master thesis.

The *refactor* package contains a rewrite of the core functionality. The goal of the rewrite was to reduce the dependency on ProbLog for query and example representations.
Different query engines can now be used as a back end for testing queries on examples, such as Django, FLGG and Subtle.
Other query engines can be added easily by implementing a wrapper with the required interface.
The *refactor* package contains its own README.md file introducing the package's content. 
Currently, it still uses some functionality from the *mai_version* package, for example for IO. 
This might be removed in a future refactor, as this could also be abstracted away from ProbLog.

## How do I get set up? ###

Pyhon 3.6 is required, since the typing module is used.
When using Django, you should have the 


### Example data sets

A couple of toy example data sets to get started with can be found in [the ACE documentation](https://dtai.cs.kuleuven.be/ACE/doc/).