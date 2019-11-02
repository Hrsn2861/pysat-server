"""views for session
"""
import utils.response as Response
from user.models import UserHelper
from user.models import PermissionHelper
from school.models import SchoolHelper

def start_session():
    """do nothing here
    """
    return Response.failed_response('Error')

def check_session(package):
    """process the request of check session
    """
    user = package.get('user')
    user = UserHelper.user_filter(user)
    if user is None:
        return Response.success_response({'user' : {}})

    user_id = user.get('id')
    permission_public = user.get('permission')
    del user['permission']
    school_id = PermissionHelper.get_user_school(user_id)
    if school_id == 0:
        school_name = 'public area'
        permission_private = -1
    else:
        school_name = SchoolHelper.get_school(school_id).get('schoolname')
        permission_private = PermissionHelper.get_permission(user_id, school_id)

    school = {
        'id' :school_id,
        'name' : school_name,
    }
    ret_user = {
        'username' : user.get('username'),
        'school' : school,
        'permission_private' : permission_private,
        'permission_public' : permission_public
    }

    return Response.success_response({'user' : ret_user})
