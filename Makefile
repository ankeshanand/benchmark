install: bin/python

bin/python:
	virtualenv benchmarkenv
	. ./benchmarkenv/bin/activate
	benchmarkenv/bin/pip install -r requirements.txt

serve: bin/python
	benchmarkenv/bin/python manage.py syncdb
	benchmarkenv/bin/python manage.py runserver 8888

deploy: benchmarkenv/bin/python
	benchmarkenv/bin/python manage.py collectstatic --clear --noinput
	touch wsgi.py # trigger reload

clean:
	rm -rf bin/ lib/ build/ dist/ *.egg-info/ include/ local/
