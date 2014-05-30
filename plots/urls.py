__author__ = 'ankesh'
import views
from django.conf.urls import patterns, url
#from plots.views import rawdata, draw

urlpatterns = patterns('',
    url(r'^(?P<plotname>[A-z]+)/$', views.draw, name='drawChart'),
    url(r'^(?P<plotname>[A-z]+)/data/$', views.rawdata, name='rawdata'),
)
