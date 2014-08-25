import os
import sys
import site

site.addsitedir('/home/benchmark/deployment/benchmark/benchmarkenv/local/lib/python2.7/site-packages')
sys.path.append('/home/benchmark/deployment')
sys.path.append('/home/benchmark/deployment/benchmark')

# Activate your virtual env
activate_env = os.path.expanduser('/home/benchmark/deployment/benchmark/benchmarkenv/bin/activate_this.py')
execfile(activate_env, dict(__file__=activate_env))
os.environ['DJANGO_SETTINGS_MODULE'] = 'benchmark.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()