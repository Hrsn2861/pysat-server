"""views for school.theme
"""
import utils.response as Response

from school.models import SubjectHelper
from utils.params import ParamType
from user.models import PermissionHelper

def create_theme(package):
    """create a theme
    """
    user = package.get('user')
    params = package.get('params')
    target_schoolid = params.get(ParamType.SchoolIdWithDefault)
    name = params.get(ParamType.ThemeName)
    msg = params.get(ParamType.ThemeDescription)
    deadline = params.get(ParamType.ThemeDeadline)

    userid = user.get('id')
    school_id = PermissionHelper.get_user_school(userid)
    private_permission = PermissionHelper.get_permission(userid, school_id)
    public_permission = user['permission']

    if public_permission > 1 and private_permission > 1:
        if target_schoolid is None:
            return Response.error_response('Invalid SchoolId')
        target_schoolid = (int)(target_schoolid)
        SubjectHelper.add_subject(target_schoolid, name, msg, deadline)
        return Response.checked_response('Create Successful')

    if public_permission > 1:
        SubjectHelper.add_subject(0, name, msg, deadline)
        return Response.checked_response('Create Successful')

    SubjectHelper.add_subject(school_id, name, msg, deadline)
    return Response.checked_response('Create Successful')
