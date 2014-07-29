from tastypie import fields, utils
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization

__author__ = 'ankesh'

from tastypie.resources import ModelResource
from fileupload.models import Picture
from django.db import models


class MultipartResource(object):
    def deserialize(self, request, data, format=None):
        if not format:
            format = request.META.get('CONTENT_TYPE', 'application/json')
        if format == 'application/x-www-form-urlencoded':
            return request.POST
        if format.startswith('multipart'):
            data = request.POST.copy()
            data.update(request.FILES)
            return data
        return super(MultipartResource, self).deserialize(request, data, format)


class PictureResource(MultipartResource, ModelResource):
    file = fields.FileField(attribute="file", null=True, blank=True)

    class Meta:
        queryset = Picture.objects.all()
        allowed_methods = ['post']
        authentication = Authentication()
        authorization = Authorization()