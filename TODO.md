# TODO

* Logging (Feature toggle to enable logging activities of the AI)
* Testing: implement unittests for all classes
* Pants: use pex to package the project
* Full test coverage: Create unittests to all classes and methods
* Create real examples with real world scenarios/test cases. Now it is possible to use the lib in experimental tests using real actions and sensors.
* Create utils classes/methods for:
  - Cloud scenarios
  - LVM and FS maintenance
  - Cleanup tasks (docker, filesystem temp files cleanup)
  - AWS Cloud formation
* Functional tests using docker
* Add costs to the actions to guarantee a better performance on long action chains.

# DONE: v0.1.0
* Action.py must implement exec() method. It will be used by the Planner to actually execute the action itself and change the environment.
* World facts must be a shared document or list in which the agent would used as knownledge base to retrieve parameters such as: which vpc id should I use while excuting some commands? Or which instance id should it use to stop the application cluster?
* The Sensor.py module needs add a class formatted sensor
* Unit Tests
* Docker (Makefile)
* Docs: Sphinx
