"""views for school.admin
"""
import utils.response as Response

from school.models import SchoolApplyHelper
from utils.params import ParamType
from user.models import UserHelper

def approve(package):
    """ Processing the request of creating a school
    """
    user = package.get('user')
    userid = user.get('id')
    params = package.get('params')
    username = params.get(ParamType.Username)

    apply_user = UserHelper.get_user_by_username(username)
    apply_userid = apply_user.get('id')
    schoolid = 1
    apply = SchoolApplyHelper.get_apply(apply_userid, schoolid)

    if apply is None:
        return Response.error_response('No Apply')

    apply_id = apply.get('id')

    status = params.get(ParamType.Approve)
    if status == 'true':
        status = 1
    else:
        status = 0

    SchoolApplyHelper.judge_apply(apply_id, userid, status)
    return Response.checked_response('Approve Successed')

def get_apply_list(package):
    """ Processing the request of getting apply list
    """
    # user = package.get('user')
    # user_id = user.get('id')
    school_id = 1 # 需要改成user所在学校

    params = package.get('params')
    list_type = params.get(ParamType.ApplyListType)
    page_num = params.get(ParamType.Page)
    if list_type is None:
        list_type = 0
    if page_num is None:
        page_num = 1
    if list_type not in [0, 1, 2]:
        return Response.error_response('Invalid list type')
    if page_num < 1:
        return Response.error_response('Invalid page number')
    apply_list = SchoolApplyHelper.get_applies(school_id, list_type, page_num)
    return Response.success_response({'list': apply_list})
