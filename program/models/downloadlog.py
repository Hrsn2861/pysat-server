"""models for download log
"""
from django.db import models
from program.models import Program #pylint: disable-msg=cyclic-import

class DownloadLog(models.Model):
    """Download Log Model
    """
    user_id = models.IntegerField()
    program_id = models.IntegerField()

    class Meta:
        verbose_name = 'download_log'
        verbose_name_plural = 'download_logs'
        get_latest_by = 'id'

class DownloadLogHelper:
    """Download Log Helper
    """
    @staticmethod
    def check_download(user_id, program_id):
        """check if user has downloaded the program or not
        """
        logs = DownloadLog.objects.filter(user_id=user_id, program_id=program_id)
        return logs.exists()

    @staticmethod
    def add_downloadlog(user_id, program_id):
        """add a download log
        """
        DownloadLog(user_id=user_id, program_id=program_id).save()

    @staticmethod
    def count_downloadlog(program_id):
        """count downloads
        """
        logs = DownloadLog.objects.filter(program_id=program_id)
        return logs.count()

    @staticmethod
    def count_user_downloadlog(user_id):
        """count user's program downloads
        """
        ret = 0
        progs = Program.objects.filter(**{
            'author' : user_id
        })
        for prog in progs:
            ret += prog.downloads

        return ret
