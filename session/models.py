"""Models about session
"""
from django.db import models

from utils import randkey
from utils import getdate_now, getdate_later

# Create your models here.

class Session(models.Model):
    """Session
    """
    token = models.CharField(max_length=128)
    ip = models.CharField(max_length=64)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    class Meta:
        verbose_name = 'session'
        verbose_name_plural = 'sessions'
        get_latest_by = 'id'

class SessionHelper:
    """Session Helper for pysat-server

    It contains some functions about session operation.
    """

    @staticmethod
    def get_session_id(token, ip_address):
        """get session id by token and ip
        """
        if not isinstance(token, str) or not isinstance(ip_address, str):
            return None
        sessions = Session.objects.filter(token=token, ip=ip_address, end_time__gt=getdate_now())
        if sessions.exists():
            session = sessions.last()
            session.end_time = getdate_later()
            session.save()
            return session.id
        return None

    @staticmethod
    def get_session_by_id(session_id):
        """get complete session by id
        """
        if not isinstance(session_id, int):
            return None
        sessions = Session.objects.filter(id=session_id)
        if sessions.exists():
            session = sessions.last()
            return {
                'id' : session.id,
                'token' : session.token,
                'ip' : session.ip,
                'start_time' : session.start_time,
                'end_time' : session.end_time
            }
        return None

    @staticmethod
    def add_session(ip_address):
        """add a session into database

        return token
        """
        if not isinstance(ip_address, str):
            return None
        token = None
        while token is None or SessionHelper.get_session_id(token, ip_address) is not None:
            token = randkey()
        Session(
            token=token,
            ip=ip_address,
            start_time=getdate_now(),
            end_time=getdate_later()
        ).save()
        return token

    @staticmethod
    def disconnect(token, ip_address):
        """disconnect a session
        """
        if not isinstance(token, str) or not isinstance(ip_address, str):
            return False
        nowdate = getdate_now()
        sessions = Session.objects.filter(token=token, ip=ip_address, end_time__gt=nowdate)
        if sessions.exists():
            session = sessions.last()
            session.end_time = nowdate
            session.save()
        return True
