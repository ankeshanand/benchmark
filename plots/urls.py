__author__ = 'ankesh'
from django.conf.urls import patterns, url
from plots.views import rawdata, draw

urlpatterns = patterns('',
    url(r'^(?P<type>[A-z]+)/$', draw, name='drawChart'),
    url(r'^(?P<type>[A-z]+)/data/$', rawdata, name='rawdata'),
)
