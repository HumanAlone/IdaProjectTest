from io import BytesIO

import urllib3
from PIL import Image
from django.core.files import File
from django.db import models


def make_image(image):
    if isinstance(image, urllib3.response.HTTPResponse):
        im = Image.open(image)
        im.convert('RGB')
        thumb_io = BytesIO()
        im.save(thumb_io, 'JPEG', quality=85)
        new_image = File(thumb_io, name="temp.jpg")
        return new_image
    return image


class NewImage(models.Model):
    image = models.ImageField(verbose_name="Файл", blank=True)
    is_copy = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.image = make_image(self.image)
        super().save(*args, **kwargs)
