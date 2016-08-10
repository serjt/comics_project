from __future__ import unicode_literals
from django.conf import settings
from django.db import models

# Create your models here.

from wand.image import Image


def file_upload_to(instance, filename):
    return "images/%s" % filename


class Comics(models.Model):
    name = models.CharField(max_length=100)
    pdf = models.FileField(upload_to=file_upload_to, null=True, blank=True)
    cover = models.ImageField(upload_to=file_upload_to, null=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(Comics, self).save()
        img = Image(filename=self.pdf._get_path())
        img.save(filename=settings.BASE_DIR + '/static_in_env/media_root/images/temp-%s-%s.jpg' % (
            self.id, self.name))
        for i in range(len(img.sequence)):
            image = ComicsImage(comics_id=self.id, image='/media/images/temp-%s-%s-%s.jpg' % (self.id, self.name, i))
            image.save()


class ComicsImage(models.Model):
    image = models.CharField(max_length=200)
    comics = models.ForeignKey(Comics)

    def __unicode__(self):
        return str(self.id)


class Coordinate(models.Model):
    x = models.DecimalField(max_digits=1000, decimal_places=2)
    y = models.DecimalField(max_digits=1000, decimal_places=2)
    h = models.DecimalField(max_digits=1000, decimal_places=2)
    w = models.DecimalField(max_digits=1000, decimal_places=2)
    image = models.ForeignKey(ComicsImage, null=True)
