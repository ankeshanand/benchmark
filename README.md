BRL-CAD Benchmarks
=========

An online platform for the BRL-CAD Benchmark Suite to view and share a detailed analysis of your systems's performace. Built with Django and Python, a GSoC '14 project. 
Originally forked from [here](http://bitbucket.org/suryajith/benchmark/)

## Screenshots

![Hi There](http://i.imgur.com/zmhV8Sk.png "Result of a Benchmark Run")

Result of a Benchmark Run

Building
============

* Clone the repository ````git clone https://github.com/BRL-CAD/benchmark.git````
* Change to the project directory ````cd benchmark````
* Swith to the development branch: ````git checkout development````
* If required, make changes to ````settings.py```` to ensure database credentials are matching with that on your system.
* Initailize a few things: ````bash ./setup.sh````
* Install and Serve the application ````make clean && make serve````
* go to ````localhost:8888/```` and upload some files

## Contact

You can usually find us at the following IRC channel : [irc://chat.freenode.net:6667/brlcad](http://webchat.freenode.net/?channels=#brlcad).
