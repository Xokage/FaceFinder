from __future__ import unicode_literals

from django.db import models

# Create your models here.

class TwitterItem(models.Model):
    account = models.CharField(verbose_name='Conta', max_length=200)
    imageUrl = models.CharField(verbose_name='Url da Imaxe', max_length=600)
    tweetUrl = models.CharField(verbose_name='Url do Tweet', max_length=600)
    occurrence = models.FloatField(verbose_name='Acerto')
    people = models.ManyToManyField('Person', blank=True)

    def __str__(self):
        return self.account




def pictures_directory_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/<name> <lastname>/<filename>
        return 'pictures/{0}/{1}'.format(instance.name + " " + instance.lastname, filename)

def refpictures_directory_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/<name> <lastname>/<filename>
        return 'pictures/{0}/{1}'.format(instance.person.name + " " + instance.person.lastname, filename)


class Person(models.Model):
    name = models.CharField(verbose_name='Nome', max_length=200)
    lastname = models.CharField(verbose_name='Apelidos', max_length=200)
    age = models.IntegerField(verbose_name='Idade')
    main_picture = models.ImageField(verbose_name='Foto', upload_to=pictures_directory_path)
    
    def __str__(self):
        return self.name + " " + self.lastname

class Picture(models.Model):
    file = models.ImageField(upload_to=refpictures_directory_path)
    person = models.ForeignKey('Person', on_delete=models.CASCADE,)
