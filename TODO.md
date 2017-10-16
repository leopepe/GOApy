# TODO

* Logging
* Create real examples with real world scenarios/test cases. Now it is possible to use the lib in experimental tests using real actions and sensors.
* Testing
* Pants: use pex to package the project

# DONE
* Action.py must implement exec() method. It will be used by the Planner to actually execute the action itself and change the environment.
* World facts must be a shared document or list in which the agent would used as knownledge base to retrieve parameters such as: which vpc id should I use while excuting some commands? Or which instance id should it use to stop the application cluster?
* The Sensor.py module needs add a class formatted sensor
* Unit Tests
* Dockerize (Makefile)
* Docs: Sphinx
