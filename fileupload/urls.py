# encoding: utf-8
from django.conf.urls import patterns, url
from fileupload.views import (
        BasicVersionCreateView, BasicPlusVersionCreateView,
        jQueryVersionCreateView, AngularVersionCreateView,
        PictureCreateView, PictureDeleteView, PictureListView,
        )
from django.http import HttpResponseRedirect

urlpatterns = patterns('',
    url(r'^$', lambda x: HttpResponseRedirect('/benchmark/upload/basic/plus/')),
    url(r'^basic/plus/$', BasicPlusVersionCreateView.as_view(), name='upload-basic-plus'),
    url(r'^delete/(?P<pk>\d+)$', PictureDeleteView.as_view(), name='upload-delete'),
    url(r'^view/$', PictureListView.as_view(), name='upload-view'),
)