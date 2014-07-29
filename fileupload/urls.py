# encoding: utf-8
from django.conf.urls import patterns, url, include
from fileupload.views import (
        BasicVersionCreateView, BasicPlusVersionCreateView,
        jQueryVersionCreateView, AngularVersionCreateView,
        PictureCreateView, PictureDeleteView, PictureListView,
        )
from django.http import HttpResponseRedirect
from tastypie.api import Api
from fileupload.api.resources import PictureResource

v1_api = Api(api_name='v1')
v1_api.register(PictureResource())

urlpatterns = patterns('',
    url(r'^$', lambda x: HttpResponseRedirect('/benchmark/upload/basic/plus/')),
    url(r'^basic/plus/$', BasicPlusVersionCreateView.as_view(), name='upload-basic-plus'),
    url(r'^delete/(?P<pk>\d+)$', PictureDeleteView.as_view(), name='upload-delete'),
    url(r'^view/$', PictureListView.as_view(), name='upload-view'),
    url(r'^api/', include(v1_api.urls)),
)