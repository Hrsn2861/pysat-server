"""models for file(not video)
"""
from django.db import models

from user.models import UserHelper

class Attechment(models.Model):
    """Attechment Model
    """
    user_id = models.IntegerField()
    filepath = models.CharField(max_length=256)
    filename = models.CharField(max_length=256)

    class Meta:
        verbose_name = 'attechment'
        verbose_name_plural = 'attechments'
        get_latest_by = 'id'

class AttechmentHelper:
    """Attechment Helper
    """
    @staticmethod
    def add_file(user_id, filepath, filename):
        """add file
        """
        attechment = Attechment(user_id=user_id, filepath=filepath, filename=filename)
        attechment.save()
        return attechment.id

    @staticmethod
    def get_file(file_id):
        """get file
        """
        qs = Attechment.objects.filter(id=file_id)
        if qs.exists():
            attechment = qs.last()
            return {
                'filename' : attechment.filename,
                'filepath' : attechment.filepath,
                'user' : UserHelper.get_name_by_id(attechment.user_id)
            }
        return None
