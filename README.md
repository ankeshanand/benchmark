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

* ````pip install -r requirements.txt```` (will install django, pillow and mysql-python)
* ````python manage.py syncdb````
* ````python manage.py runserver````
* go to ````localhost:8000/upload/new/```` and upload some files
