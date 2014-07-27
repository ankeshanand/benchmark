benchmark
=========

Visualization and Database framework for BRL-CAD's benchmarks, a GSoC '14 project. 
Originally forked from [here](http://bitbucket.org/suryajith/benchmark/)



Installation
============

* Clone the repository ````git clone https://github.com/BRL-CAD/benchmark.git````
* Change to the project directory ````cd benchmark````
* Swith to the development branch: ````git checkout development````
* If required, make changes to ````settings.py```` to ensure database credentials are matching with that on your system.
* Initailize a few things: ````bash ./setup.sh````
* Install and Serve the application ````make clean && make serve````
* go to ````localhost:8888/```` and upload some files
