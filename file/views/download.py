"""
module for downloading file
"""
import re

from django.http import StreamingHttpResponse, FileResponse

from utils.params import ParamType
from utils.file import file_iterator
from file.models import VideoHelper

def video(package):
    """method for download video
    """
    params = package.get('params')
    video_id = params.get(ParamType.VideoID)

    request = package.get('request')
    range_header = request.META.get('HTTP_RANGE', '').strip()
    range_re = re.compile(r'bytes\s*=\s*(\d+)\s*-\s*(\d*)', re.I)
    range_match = range_re.match(range_header)

    videoinfo = VideoHelper.get_video(video_id)
    filepath = videoinfo['filepath']
    filesize = videoinfo['size']

    if range_match:
        first_byte, last_byte = range_match.groups()
        first_byte = int(first_byte) if first_byte else 0
        last_byte = first_byte + 1024 * 1024 * 8
        if last_byte >= filesize:
            last_byte = filesize - 1
        length = last_byte - first_byte + 1
        response = StreamingHttpResponse(
            file_iterator(filepath, offset=first_byte, length=length), status=206)
        response['Content-Length'] = str(length)
        response['Content-Range'] = 'bytes %s-%s/%s' % (first_byte, last_byte, filesize)
    else:
        response = FileResponse(open(filepath, 'rb'))
        response['Content-Length'] = str(filesize)
    response['Content-Type'] = 'video/mp4'
    response['Content-Disposition'] = 'attachment;filename="' + videoinfo['filename'] + '"'
    response['Accept-Ranges'] = 'bytes'
    return response
