__author__ = 'ankesh'

from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    url(r'^(?P<filename>[a-zA-Z0-9]+)/$', views.show_result, name='showResult'),
)

