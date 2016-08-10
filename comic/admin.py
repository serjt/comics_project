from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Comics)
admin.site.register(ComicsImage)


class CoordinatesAdmin(admin.ModelAdmin):
    model = Coordinate
    list_display = 'x y w h image'.split()


admin.site.register(Coordinate,CoordinatesAdmin)
