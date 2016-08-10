from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from .models import *
from tastypie import fields


class CoordinateResource(ModelResource):
    class Meta:
        queryset = Coordinate.objects.all()
        resource_name = 'coordinates'


class ImageResource(ModelResource):
    coordinates = fields.ManyToManyField(CoordinateResource, 'coordinates', null=True, full=True)

    class Meta:
        queryset = ComicsImage.objects.all()
        resource_name = 'image'
        filtering = {
            'id': ALL_WITH_RELATIONS,
        }


class DataResource(ModelResource):
    class Meta:
        queryset = UploadComics.objects.all()
        resource_name = 'general'


class ComicsResource(ModelResource):
    general = fields.OneToOneField(DataResource, 'general', null=True, full=True)
    pages = fields.ManyToManyField(ImageResource, 'pages', null=True, full=True)

    class Meta:
        queryset = Comics.objects.all()
        resource_name = 'comics'
        filtering = {
            'id': ALL_WITH_RELATIONS,
        }
