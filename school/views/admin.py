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
