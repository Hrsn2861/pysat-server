"""views for user.info
"""

import utils.response as Response

from utils.params import ParamType
from user.models import UserHelper
from user.models import VerifyHelper

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
        return Response.error_response("No User")

    info = {
        "realname" : realname,
        "school" : school,
        "motto" : motto,
        "permission" : int(permission)
    }
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
