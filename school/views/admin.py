"""views for school.admin
"""
import utils.response as Response

from school.models import SchoolApplyHelper
from utils.params import ParamType
from user.models import PermissionHelper

def approve(package):
    """ Processing the request of creating a school
    """
    user = package.get('user')
    params = package.get('params')
    user_id = user.get('id')
    school_id = PermissionHelper.get_user_school(user_id)
    if school_id == 0:
        return Response.error_response("You are not in a school")

    params = package.get('params')
    apply_id = int(params.get(ParamType.ApplyId))

    apply = SchoolApplyHelper.get_apply_by_id(apply_id)
    apply_user_id = apply.get('userid')
    if apply is None:
        return Response.error_response('No Apply')

    status = params.get(ParamType.Approve)
    if status == 'true':
        status = 1
    else:
        status = 0

    SchoolApplyHelper.judge_apply(apply_id, user_id, status)
    PermissionHelper.user_join_school(apply_user_id, school_id)
    return Response.checked_response('Approve Successed')

def get_apply_list(package):
    """ Processing the request of getting apply list
    """
    user = package.get('user')
    user_id = user.get('id')
    school_id = PermissionHelper.get_user_school(user_id)
    if school_id == 0:
        return Response.error_response("You are not in a school")

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
