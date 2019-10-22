"""models for program like
"""
from django.db import models

class Like(models.Model):
    """Program Like Model
    """
    user_id = models.IntegerField()
    program_id = models.IntegerField()

    class Meta:
        verbose_name = 'program_like'
        verbose_name_plural = 'program_likes'
        get_latest_by = 'id'

class LikeHelper:
    """Program Like Helper
    """
    @staticmethod
    def check_like(user_id, program_id):
        """check if user has liked the program or not
        """
        logs = Like.objects.filter(user_id=user_id, program_id=program_id)
        return logs.exists()

    @staticmethod
    def add_like(user_id, program_id):
        """add a like log
        """
        Like(user_id=user_id, program_id=program_id).save()
