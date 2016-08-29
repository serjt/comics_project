import json
import os
from django import forms
from django.forms import ModelForm
from django.contrib import admin
from django.forms.widgets import TextInput
from django.template import Template, Context
from .models import *
from comics_project.settings import BASE_DIR


class ComicsSujetWidget(TextInput):
    def render(self, name, value, attrs=None):
        file_res = open(os.path.join(BASE_DIR, 'templates/widget/cswidget.html'))
        content = file_res.read()
        file_res.close()

        template = Template(content)
        if self.form_instance.instance.id is None:
            return template.render(Context(dict(new=True, attrs=attrs, name=name, value=value)))

        obj = ComicsImage.objects.get(id=self.form_instance.instance.id)
        return template.render(Context(dict(new=False, object=obj, attrs=attrs, name=name, value=value)))


class ComicsImageForm(ModelForm):
    coordinates_json = forms.CharField(widget=ComicsSujetWidget())

    def __init__(self, *args, **kwargs):
        super(ComicsImageForm, self).__init__(*args, **kwargs)
        self.fields['coordinates_json'].widget.form_instance = self


class ComicsImageAdmin(admin.ModelAdmin):
    form = ComicsImageForm
    exclude = ['coordinates', 'image']

    def save_model(self, request, obj, form, change):
        comics_image = ComicsImage.objects.get(id=obj.id)
        coordinates = json.loads(request.POST.get('coordinates_json'))
        print(coordinates)

        for item in coordinates:
            print(item)
            coordinate = Coordinate()
            coordinate.x = item['x']
            coordinate.y = item['y']
            coordinate.w = item['w']
            coordinate.h = item['h']

            coordinate.save()
            comics_image.coordinates.add(coordinate)

        comics_image.save()

        super(ComicsImageAdmin, self).save_model(request, obj, form, change)


# Register your models here.
admin.site.register(Comics)
admin.site.register(ComicsImage, ComicsImageAdmin)
admin.site.register(Coordinate)
admin.site.register(UploadComics)
