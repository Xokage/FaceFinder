from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Person(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Image(models.Model):
    url = models.CharField(max_length=600)

    def __str__(self):
        return self.url

class Image_Occurrence(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
