"""VerifyCode Helper for pysat-server

* It contains some functions about VerifyCode operation.
"""

from django.db.models import Q

from server.models import VerifyCode
from server.utils.utils import randkey, getdate_now
from server.utils.models.user import UserInfoChecker


def get_latest_code(session_id, phone):
    """get the latest code
    """
    if not isinstance(session_id, int):
        return None
    if UserInfoChecker.check_phone(phone) is not True:
        return None
    logs = VerifyCode.objects.filter(
        session_id=session_id,
        phone=phone
    ).filter(~Q(code=''))
    if logs.exists():
        log = logs.last()
        return {
            'code' : log.code,
            'time' : log.send_time
        }
    return None


def del_codes(session_id, phone):
    """delete all codes with `seesion_id` and `phone`.
    """
    if not isinstance(session_id, int):
        return False
    if UserInfoChecker.check_phone(phone) is not True:
        return False
    logs = VerifyCode.objects.filter(
        session_id=session_id,
        phone=phone
    )
    for log in logs:
        log.code = ""
        log.save()
    return True


def add_code(session_id, phone):
    """get the EntryLog by session_id.
    """
    if not del_codes(session_id, phone):
        return None

    code = "GUXYNB" # randkey(length=6)
    VerifyCode(
        session_id=session_id,
        phone=phone,
        code=code,
        send_time=getdate_now()
    ).save()

    return code


def check_code(session_id, phone, code):
    """check the verify_code
    """
    if not isinstance(session_id, int):
        return False
    if not isinstance(code, str) or code == "":
        return False
    if UserInfoChecker.check_phone(phone) is not True:
        return False
    logs = VerifyCode.objects.filter(
        session_id=session_id,
        phone=phone,
        code=code
    )
    if logs.exists():
        log = logs.last()
        log.code = ""
        log.save()
        return True
    return False
