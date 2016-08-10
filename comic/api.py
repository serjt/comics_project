from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from .models import *
from tastypie import fields


class ComicsResource(ModelResource):
    class Meta:
        queryset = Comics.objects.all()
        resource_name = 'comics'
        excludes = 'pdf'.split()
        filtering = {
            'id':ALL_WITH_RELATIONS,
        }


class ImageResource(ModelResource):
    comics = fields.ForeignKey(ComicsResource, 'comics', null=True)

    class Meta:
        queryset = ComicsImage.objects.all()
        resource_name = 'image'
        filtering = {
            'id': ALL_WITH_RELATIONS,
            'comics':ALL_WITH_RELATIONS
        }


class CoordinateResource(ModelResource):
    image = fields.ForeignKey(ImageResource, 'image', null=True)

    class Meta:
        queryset = Coordinate.objects.all()
        resource_name = 'coordinates'
        filtering = {
            'image': ALL_WITH_RELATIONS
        }
