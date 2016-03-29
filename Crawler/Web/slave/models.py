from __future__ import unicode_literals

from django.db import models

# Create your models here.

class TwitterItem(models.Model):
    account = models.CharField(max_length=200)
    imageUrl = models.CharField(max_length=600)
    tweetUrl = models.CharField(max_length=600)
    occurrence = models.FloatField()

    def __str__(self):
        return self.account
