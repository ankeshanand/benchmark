import os
import sys
import site

site.addsitedir('/var/www/benchmark/lib/python2.7/site-packages')
sys.path.append('/var/www')
sys.path.append('/var/www/benchmark')

os.environ['DJANGO_SETTINGS_MODULE'] = 'benchmark.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()