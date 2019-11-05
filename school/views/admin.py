"""views for school.admin
"""
import utils.response as Response

from utils.params import ParamType
from utils.permission import PermissionManager, ActionType
from school.models import SchoolApplyHelper, SchoolHelper
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
    permission = PermissionHelper.get_permission(user_id, school_id)
    if not PermissionManager.check_permission(permission, ActionType.Approve):
        return Response.error_response('Access Denied')

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
        status = 2

    SchoolApplyHelper.judge_apply(apply_id, user_id, status)
    PermissionHelper.user_join_school(apply_user_id, school_id)
    return Response.checked_response('Approve Successed')

def get_apply_list(package):
    # pylint: disable-msg=too-many-return-statements
    """ Processing the request of getting apply list
    """
    user = package.get('user')
    if user is None:
        return Response.error_response('No User')
    user_id = user.get('id')
    # school_id = PermissionHelper.get_user_school(user_id)

    params = package.get('params')
    list_type = params.get(ParamType.ApplyListType)
    page_num = params.get(ParamType.Page)
    target_schoolid = int(params.get(ParamType.SchoolId))

    if target_schoolid == 0:
        return Response.error_response('Invalid SchoolId')

    permission = PermissionHelper.get_permission(user_id, target_schoolid)
    if not PermissionManager.check_permission(permission, ActionType.GetApplyList):
        return Response.error_response('Access Denied')

    if list_type is None:
        list_type = 0
    list_type = int(list_type)
    if page_num is None:
        page_num = 1
    page_num = int(page_num)
    if list_type not in [0, 1, 2]:
        return Response.error_response('Invalid list type')
    if page_num < 1:
        return Response.error_response('Invalid page number')
    apply_list = SchoolApplyHelper.get_applies(target_schoolid, list_type, page_num)

    school = SchoolHelper.get_school(target_schoolid)
    if school is None:
        return Response.error_response('No School')

    ret = {
        'tot_count' : SchoolApplyHelper.get_applies_count(target_schoolid, list_type),
        'now_count' : len(apply_list),
        'apply_list' : apply_list
    }
    return Response.success_response(ret)
