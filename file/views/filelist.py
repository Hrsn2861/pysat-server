"""
module for getting file list
"""
import utils.response as Response

from utils.params import ParamType
from utils.listhelper import get_list
from file.models import Video, VideoHelper

def info(package):
    """method for download video
    """
    params = package.get('params')
    school_id = params.get(ParamType.SchoolId)
    category_id = params.get(ParamType.CategoryId)
    page = params.get(ParamType.Page)
    if page is None:
        page = '1'
    page = int(page)
    if page <= 0:
        page = 1
    selector = VideoHelper.get_video_filter(school_id, category_id)
    count, videos = get_list(
        Video, selector, VideoHelper.video_to_dict, page,
        hide_list=['filepath'])
    return Response.success_response({
        'tot_count' : count,
        'now_count' : len(videos),
        'video_list' : videos
    })
