"""Models about entrylog
"""
from django.db import models
from django.utils import timezone

class EntryLog(models.Model):
    """EntryLog
    """
    session_id = models.IntegerField()
    user_id = models.IntegerField()
    login_time = models.DateTimeField()
    logout_time = models.DateTimeField()

    class Meta:
        verbose_name = 'log'
        verbose_name_plural = 'logs'
        get_latest_by = 'id'

class EntryLogHelper:
    """User Helper for pysat-server

    It contains some functions about user operation.
    """

    @staticmethod
    def get_entrylog(session_id):
        """get the EntryLog by session_id.
        """
        if not isinstance(session_id, int):
            return None
        logs = EntryLog.objects.filter(
            session_id=session_id,
            logout_time__gt=timezone.now()
        )
        if logs.exists():
            log = logs.last()
            return {
                'id' : log.id,
                'session_id' : log.session_id,
                'user_id' : log.user_id,
                'login_time' : log.login_time,
                'logout_time' : log.logout_time
            }
        return None

    @staticmethod
    def get_entrylog_by_user(user_id):
        """get the EntryLog by user_id.
        """
        if not isinstance(user_id, int):
            return None
        logs = EntryLog.objects.filter(
            user_id=user_id,
            logout_time__gt=timezone.now()
        )
        if logs.exists():
            log = logs.last()
            return {
                'id' : log.id,
                'session_id' : log.session_id,
                'user_id' : log.user_id,
                'login_time' : log.login_time,
                'logout_time' : log.logout_time
            }
        return None

    @staticmethod
    def del_entrylog(session_id=None, user_id=None):
        """logout the entrylogs about `session_id` and `user_id`
        """
        nowdate = timezone.now()
        if isinstance(session_id, int):
            logs = EntryLog.objects.filter(
                session_id=session_id, logout_time__gt=nowdate)
            for log in logs:
                log.logout_time = nowdate
                log.save()
        if isinstance(user_id, int):
            logs = EntryLog.objects.filter(
                user_id=user_id, logout_time__gt=nowdate)
            for log in logs:
                log.logout_time = nowdate
                log.save()

    @staticmethod
    def add_entrylog(session_id, user_id):
        """Add an EntryLog into database.

        Return a random key.
        """
        if not isinstance(session_id, int) or not isinstance(user_id, int):
            return False
        EntryLogHelper.del_entrylog(session_id=session_id, user_id=user_id)

        nowdate = timezone.now()

        EntryLog(
            session_id=session_id,
            user_id=user_id,
            login_time=nowdate,
            logout_time=nowdate + timezone.timedelta(days=7)
        ).save()

        return True
