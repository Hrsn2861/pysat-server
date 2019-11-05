"""
module for downloading file
"""
from django.http import FileResponse

from utils.params import ParamType
from file.models import VideoHelper

def video(package):
    """method for download video
    """
    params = package.get('params')
    video_id = params.get(ParamType.VideoID)

    videoinfo = VideoHelper.get_video(video_id)
    filepath = videoinfo['filepath']

    response = FileResponse(open(filepath, 'rb'))
    response['Content-Type'] = 'video/mpeg4'
    response['Content-Disposition'] = 'attachment;filename="' + videoinfo['filename'] + '"'
    return response
