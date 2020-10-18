# TODO

* Full test coverage: Create unittests to all classes and methods (Need to check real coverage)
* PyDocs in all functions/methods
* Auto generate documentation from pydocs (sphynx)
* Logging (Feature toggle to enable logging activities of the AI)
* Create real examples with real world scenarios/test cases. Now it is possible to use the lib in experimental tests using real actions and sensors.
  * Create utils classes/methods for:
    - Cloud scenarios
    - LVM and FS maintenance
    - Cleanup tasks (docker, filesystem temp files cleanup)
    - AWS Cloud formation
* Change Planner so the adding nodes and edges would follow the implementation described in https://www.datacamp.com/community/tutorials/networkx-python-graph-tutorial (CSV or table based import. Useful when using config files to generate the automaton)

# DONE: v0.2.1
* Refactor Actions and Sensors to receive func: Callable as parameter (no more ShellCommandAction and ObjectAction)
* Add costs to the actions to guarantee a better performance on long action chains.
* Code quality increased to A level on Codacy
* Test coverage increased to 81%

# DONE: v0.2.0
* Testing: implement unittests for all classes
* Build with travis-ci
* Enable coveralls.io

# DONE: v0.1.0
* Action.py must implement exec() method. It will be used by the Planner to actually execute the action itself and change the environment.
* World facts must be a shared document or list in which the agent would used as knownledge base to retrieve parameters such as: which vpc id should I use while excuting some commands? Or which instance id should it use to stop the application cluster?
* The Sensor.py module needs add a class formatted sensor
* Unit Tests
* Docker (Makefile)
* Docs: Sphinx
