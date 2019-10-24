"""Models about verify
"""
from django.db import models

from utils import getdate_now, randkey
from utils.checker import UserInfoChecker

class VerifyCode(models.Model):
    """VerifyCode
    """
    session_id = models.IntegerField()
    phone = models.CharField(max_length=11)
    code = models.CharField(max_length=8)
    send_time = models.DateTimeField()

    class Meta:
        verbose_name = 'verifycode'
        verbose_name_plural = 'verifycodes'
        get_latest_by = 'id'

class VerifyHelper:
    """User Helper for pysat-server

    It contains some functions about user operation.
    """

    @staticmethod
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
        ).filter(~models.Q(code=''))
        if logs.exists():
            log = logs.last()
            return {
                'code' : log.code,
                'time' : log.send_time
            }
        return None

    @staticmethod
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
            log.code = ''
            log.save()
        return True

    @staticmethod
    def add_code(session_id, phone, default_code='GUXYNB'):
        """get the EntryLog by session_id.
        """
        if not VerifyHelper.del_codes(session_id, phone):
            return None

        if default_code is None:
            code = randkey(length=6)
        else:
            code = default_code
        VerifyCode(
            session_id=session_id,
            phone=phone,
            code=code,
            send_time=getdate_now()
        ).save()

        return code

    @staticmethod
    def check_code(session_id, phone, code):
        """check the verify_code
        """
        if not isinstance(session_id, int):
            return False
        if not isinstance(code, str) or code == '':
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
            log.code = ''
            log.save()
            return True
        return False
