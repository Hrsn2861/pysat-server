"""models for video
"""
from django.db import models

from utils import getdate_now
from user.models import UserHelper

class Video(models.Model):
    """Video Model
    """
    title = models.CharField(max_length=64)
    description = models.TextField()
    filename = models.CharField(max_length=256)
    filepath = models.CharField(max_length=256)
    school = models.IntegerField()
    category = models.IntegerField()
    uploader = models.IntegerField()
    upload_time = models.DateTimeField()
    video_size = models.IntegerField()

    class Meta:
        verbose_name = 'video'
        verbose_name_plural = 'videos'
        get_latest_by = 'id'

class VideoHelper:
    """Video Helper
    """
    # pylint:disable-msg=too-many-arguments
    @staticmethod
    def add_video(user_id, title, description, filename, filepath, school, category, video_size):
        """add video
        """
        video = Video(
            uploader=user_id,
            title=title,
            filename=filename,
            filepath=filepath,
            description=description,
            school=school,
            category=category,
            video_size=video_size,
            upload_time=getdate_now())
        video.save()
        return video.id

    @staticmethod
    def video_to_dict(video):
        """video to dict
        """
        return {
            'id' : video.id,
            'name' : video.title,
            'description' : video.description,
            'upload_time' : video.upload_time,
            'size' : video.video_size,
            'filename' : video.filename,
            'filepath' : video.filepath,
            'school' : video.school,
            'user' : UserHelper.get_name_by_id(video.uploader),
            'category' : video.category
        }

    @staticmethod
    def get_video(video_id):
        """get video
        """
        qs = Video.objects.filter(id=video_id)
        if qs.exists():
            video = qs.last()
            return VideoHelper.video_to_dict(video)
        return None

    @staticmethod
    def get_video_filter(school_id, category_id):
        """get a filter
        """
        ret = {}
        if school_id is not None:
            ret['school'] = school_id
        if category_id is not None:
            ret['category'] = category_id
        return ret

    @staticmethod
    def get_video_count(school_id, category_id):
        """get count
        """
        return Video.objects.filter(VideoHelper.get_video_filter(school_id, category_id)).count()

    @staticmethod
    def get_video_list(school_id, category_id, page):
        """get list
        """
        qs = Video.objects.filter(VideoHelper.get_video_filter(school_id, category_id))
        qs = qs[(page - 1) * 20 : page * 20]
        videos = []
        for video in qs:
            videos.append(VideoHelper.video_to_dict(video))
        return videos
