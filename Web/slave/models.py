# -*- coding: utf-8 -*-
#################################################################################
#   Facefinder: Crawl pictures based on known faces and extract information.    #
#   Copyright (C) 2016 Xoán Antelo Castro                                       #
#                                                                               #
#   This program is free software: you can redistribute it and/or modify        #
#   it under the terms of the GNU General Public License as published by        #
#   the Free Software Foundation, either version 3 of the License, or           #
#   (at your option) any later version.                                         #
#                                                                               #
#   This program is distributed in the hope that it will be useful,             #
#   but WITHOUT ANY WARRANTY; without even the implied warranty of              #
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
#   GNU General Public License for more details.                                #
#                                                                               #
#   You should have received a copy of the GNU General Public License           #
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.       #
#################################################################################

from django.db import models


#MODELS UTIL
def pictures_directory_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/<name> <lastname>/<filename>
        return 'pictures/{0}/main_picture/{1}'.format(instance.name + " " + instance.lastname, filename)

def refpictures_directory_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/<name> <lastname>/<filename>
        return 'pictures/{0}/reference_pictures/{1}'.format(instance.person.name + " " + instance.person.lastname, filename)


# MODELS

class TwitterItem(models.Model):
    account = models.CharField(verbose_name='Conta', max_length=200)
    imageUrl = models.CharField(verbose_name='Url da Imaxe', max_length=600)
    tweetUrl = models.CharField(verbose_name='Url do Tweet', max_length=600)
    occurrence = models.FloatField(verbose_name='Acerto')
    people = models.ManyToManyField('Person', blank=True)

    def __str__(self):
        return self.account

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
