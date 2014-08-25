__author__ = 'ankesh'

from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    url(r'^(?P<filename>[a-zA-Z0-9]+)/$', views.show_result, name='showResult'),
    url(r'^compare/(?P<filename>[a-zA-Z0-9]+)/$', views.compare_result, name='compareResult'),
    url(r'^recent/$', views.recent_results, name='recentResults'),
)

