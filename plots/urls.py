__author__ = 'ankesh'
import views
from django.conf.urls import patterns, url
from django.views.generic import TemplateView
#from plots.views import rawdata, draw

urlpatterns = patterns('',
    url(r'/^(?P<plotname>[A-z]+)/$', views.draw, name='drawChart'),
    url(r'/^(?P<plotname>[A-z]+)/data/$', views.rawdata, name='rawdata'),
    url(r'/^$', TemplateView.as_view(template_name='index.html'))
)
