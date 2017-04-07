from __future__ import unicode_literals

from django.db import models

class Tweets(models.Model):
    longitude = models.CharField(max_length=20)
    latitude = models.CharField(max_length=20)
    keywords = models.CharField(max_length=150)
    post_time = models.DateTimeField()
