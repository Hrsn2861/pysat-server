"""Session Helper for pysat-server

* It contains some functions about session operation.
"""

import random
from django.utils import timezone

from server.models import Session


def randkey(length=128):
    """generate a random key
    """
    key = ''
    for _ in range(length):
        key += chr(random.randint(65, 90))
    return key


def get_session_id(token, ip_address):
    """get session id by token and ip
    """
    if not isinstance(token, str) or not isinstance(ip_address, str):
        return None
    nowdate = timezone.now()
    sessions = Session.objects.filter(token=token, ip=ip_address, end_time__gt=nowdate)
    if sessions.exists():
        session = sessions.last()
        session.end_time = nowdate + timezone.timedelta(days=7)
        session.save()
        return session.id
    return None


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


def add_session(ip_address):
    """add a session into database

    return token
    """
    
    if not isinstance(ip_address, str):
        return None
    token = None
    while token is None or get_session_id(token, ip_address) is not None:
        token = randkey()

    nowdate = timezone.now()

    Session(
        token=token,
        ip=ip_address,
        start_time=nowdate,
        end_time=nowdate + timezone.timedelta(days=7)
    ).save()

    return token


def disconnect(token, ip_address):
    """disconnect a session
    """
    if not isinstance(token, str) or not isinstance(ip_address, str):
        return False
    nowdate = timezone.now()
    sessions = Session.objects.filter(token=token, ip=ip_address, end_time__gt=nowdate)
    if sessions.exists():
        session = sessions.last()
        session.end_time = nowdate
        session.save()
    return True
