"""views for user.info
"""

import utils.response as Response

from school.models import SchoolHelper
from utils.params import ParamType
from utils.permission import PermissionManager
from user.models import PermissionHelper
from user.models import UserHelper
from user.models import VerifyHelper
from program.models import DownloadLogHelper

def get_info(package):
    """process the request of getting user's info
    """
    params = package.get('params')
    username = params.get(ParamType.UsernameWithDefault)
    if username is None:
        user = package.get('user')
    else:
        user = UserHelper.get_user_by_username(username)
    if user is None:
        return Response.error_response("No User")

    user = UserHelper.user_filter(user)
    permission_public = user.get('permission')
    user_id = user.get('id')
    school_id = PermissionHelper.get_user_school(user_id)
    if school_id == 0:
        schoolname = 'public area'
        permission_private = -1
    else:
        permission_private = PermissionHelper.get_permission(user_id, school_id)
        school = SchoolHelper.get_school(school_id)
        schoolname = school.get('schoolname')

    download = DownloadLogHelper.count_user_downloadlog(user_id)

    del user['permission']
    user.update({
        'school_name' : schoolname,
        'permission_public' : permission_public,
        'permission_pirvate' : permission_private,
        'download' : download
    })
    return Response.success_response({'user' : user})

def modify_info(package):
    """Process the request of modyfying user's info
    """
    params = package.get('params')
    username = params.get(ParamType.UsernameWithDefault)
    realname = params.get(ParamType.RealnameForModify)
    school = params.get(ParamType.SchoolForModify)
    motto = params.get(ParamType.MottoForModify)
    permission = params.get(ParamType.PermissionForModify)
    if username is None:
        user = package.get('user')
    else:
        user = UserHelper.get_user_by_username(username)
    if user is None:
        return Response.error_response('No User')

    info = {
        'realname' : realname,
        'school' : school,
        'motto' : motto
    }
    if permission is not None:
        info['permission'] = int(permission)
    info = {k : v for k, v in info.items() if v is not None}
    action = PermissionManager.modify_to_action(package.get('user'), user, info)
    if not PermissionManager.check_user(package.get('user'), action):
        return Response.error_response('Access Denied')
    UserHelper.modify_user(user.get('id'), info)
    return Response.success_response(None)

def set_phone(package):
    """process the request of modifying user's phone
    """
    params = package.get('params')
    phone = params.get(ParamType.Phone)
    code = params.get(ParamType.CAPTCHA)
    session = package.get('session')
    user = package.get('user')
    if not VerifyHelper.check_code(session, phone, code):
        return Response.error_response("CAPTCHA Error")
    UserHelper.modify_user(user['id'], {'phone' : phone})
    return Response.checked_response("Success")
