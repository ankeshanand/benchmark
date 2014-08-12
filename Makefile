install: bin/python

bin/python:
	virtualenv benchmarkenv
	source ./benchmarkenv/bin/activate
	bin/pip install -r requirements.txt

serve: bin/python
	bin/python manage.py syncdb
	bin/python manage.py runserver 8888

deploy: bin/python
	bin/python manage.py collectstatic --clear --noinput
	touch wsgi.py  # trigger reload

clean:
	rm -rf bin/ lib/ build/ dist/ *.egg-info/ include/ local/
