"""Session Helper for pysat-server

* It contains some functions about session operation.
"""


from server.models import Session
from server.utils.utils import randkey
from server.utils.utils import getdate_now, getdate_later


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

    Session(
        token=token,
        ip=ip_address,
        start_time=getdate_now(),
        end_time=getdate_later()
    ).save()

    return token


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
