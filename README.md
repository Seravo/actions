# actions
Misc tests for GitHub actions to have much simpler implementations of certain features.


## Goals

 - reduce duplication: define actions once, and reuse in workflows
 - prevent vendor locking: avoid too hard dependencies on any external build
   tooling, try to complete tasks with shell-script based solutions when
   feasible
