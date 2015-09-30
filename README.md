Untold
======

A little engine to run interactive stories. 

DEVELOPMENT HINTS
-----------------

* Instead of manipulating nodes directly, always create referential copies
  instead. Later evaluations of the same node might have to create different
  evaluations of them.
* When implementing tags that take lists at argument, process those with
  untold.scripting.eval_list_node(node_list, state) before proceeding.

KNOWN BUGS
----------

* Example stories are likely highly buggy due to changes in the scripting
  syntax.

TODO
----

##### "I'm working on that right now!"
* 'set' should have explicit timing; several consecutive steps of parallel computations.

#### Language features
* Abstract functions: Expressions that are defined at document level, then each
  can be used by several expression-using subnodes.
* i18n/l10n and templating

##### REPL features
* Rewind / Forward
* Inspecting / Editing of document / current node / current state
* readline interface instead of raw_input()
  * tab completion
  * automatic creation of matching parens / node stubs

##### Tools
* Proper story_writer
  * yaml2json story converter (come on, it's just loads() and dumps())
  * Some syntax checking (re: story syntax)
* Syntax checker
  * Warnings when multiple evaluatable keys are used in root nodes
* Web-based story authoring / debugging / publishing tool

##### Minor enhancements
* Conditions
  * any/all/at-least-n/at-most-n for lists of conditions
  * Fold conditions and scripting nodes into a uniform system
* Syntax
  * choice weights
    * variable-stores values
    * variables-stored values weighted by constants
    * conditions as weights?
* Debugging
  * Improve Exceptions with Node IDs
  * Catch and override CaseWithoutActiveCond
* Add typechecking everywhere applicable
      from types import *
      assert foo is IntType, "foo is %s, not Int" % (type(foo), )

##### Tests
* A Choice where Weights are expressions
* An actable with a set where the var is an expression.

##### Documentation
* Story syntax (JSON and YAML)
  * Remove the stub from story_writer
