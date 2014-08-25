__author__ = 'ankesh'
from django.conf.urls import patterns, include, url
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'upload.views.home', name='home'),

    url(r'^$', TemplateView.as_view(template_name="home.html")),
    url(r'^upload/', include('fileupload.urls')),
    url(r'^plots/', include('plots.urls')),
    url(r'^result/', include('results.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

import os
urlpatterns += patterns('',
    (r'^media/(.*)$', 'django.views.static.serve', {'document_root': os.path.join(os.path.abspath(os.path.dirname(__file__)), 'media')}),
)
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()