benchmark
=========

Visualization and Database framework for BRL-CAD's benchmarks, a GSoC '14 project. 
Originally forked from [here](http://bitbucket.org/suryajith/benchmark/)

Requirements
============

* Django
* Pillow
* mysql-python

Installation
============

* Clone the repository ````git clone https://github.com/ankeshanand/benchmark.git````
* ````cd benchmark````
* ````pip install -r requirements.txt```` (will install django, pillow and mysql-python)
* ````python manage.py syncdb````
* ````python manage.py runserver````
* go to ````localhost:8000/```` and upload some files
