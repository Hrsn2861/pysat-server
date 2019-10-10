"""Models for pysat
"""

from django.db import models

# Create your models here.

class User(models.Model):
    """User
    """
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=128)
    email = models.CharField(max_length=64)
    telphone = models.CharField(max_length=11)

    realname = models.CharField(max_length=32)
    school = models.CharField(max_length=64)

    permission = models.IntegerField()

    motto = models.CharField(max_length=256, default="")

    valid = models.BooleanField(default=True)
    verify = models.CharField(max_length=6, default="")


class EntryLog(models.Model):
    """EntryLog
    """
    userid = models.IntegerField()
    key = models.CharField(max_length=128)
    entrytime = models.DateTimeField()
    deadtime = models.DateTimeField()
