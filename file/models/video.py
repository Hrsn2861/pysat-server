"""models for video
"""
from django.db import models

from user.models import UserHelper

class Video(models.Model):
    """Video Model
    """
    title = models.CharField(max_length=64)
    description = models.TextField()
    filepath = models.CharField(max_length=256)
    school = models.IntegerField()
    user_id = models.IntegerField()

    class Meta:
        verbose_name = 'video'
        verbose_name_plural = 'videos'
        get_latest_by = 'id'

class VideoHelper:
    """Video Helper
    """
    @staticmethod
    def add_file(user_id, title, description, filepath, school):
        """add file
        """
        video = Video(
            user_id=user_id,
            title=title,
            filepath=filepath,
            description=description,
            school=school)
        video.save()
        return video.id

    @staticmethod
    def get_file(file_id):
        """get file
        """
        qs = Video.objects.filter(id=file_id)
        if qs.exists():
            video = qs.last()
            return {
                'title' : video.title,
                'description' : video.description,
                'filepath' : video.filepath,
                'school' : video.school,
                'user' : UserHelper.get_name_by_id(video.user_id)
            }
        return None
