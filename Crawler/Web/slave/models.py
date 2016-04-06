from __future__ import unicode_literals

from django.db import models

# Create your models here.

class TwitterItem(models.Model):
    account = models.CharField(verbose_name='Conta', max_length=200)
    imageUrl = models.CharField(verbose_name='Url da Imaxe', max_length=600)
    tweetUrl = models.CharField(verbose_name='Url do Tweet', max_length=600)
    occurrence = models.FloatField(verbose_name='Acerto')

    def __str__(self):
        return self.account
