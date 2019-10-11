"""Models for pysat
"""

from django.db import models

# Create your models here.

class User(models.Model):
    """User
    """
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=128)
    phone = models.CharField(max_length=11)

    email = models.CharField(max_length=64, default="")
    email_verify = models.CharField(max_length=64, default="")

    realname = models.CharField(max_length=32, default="")
    school = models.CharField(max_length=64, default="")
    motto = models.CharField(max_length=256, default="")

    permission = models.IntegerField(default=1)


class Session(models.Model):
    """Session
    """
    token = models.CharField(max_length=128)
    ip = models.CharField(max_length=64)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()


class EntryLog(models.Model):
    """EntryLog
    """
    session_id = models.IntegerField()
    user_id = models.IntegerField()
    login_time = models.DateTimeField()
    logout_time = models.DateTimeField()
