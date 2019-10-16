"""views for user.sign
"""

import utils.response as Response
import utils.code_sender.phone as PhoneSender
import utils.code_sender.email as EmailSender

from utils import getdate_now
from utils.params import ParamType
from utils.checker import UserInfoChecker
from user.models import UserHelper
from user.models import VerifyHelper
from user.models import EntryLogHelper
from server.models import ConfigHelper


def signin(package):
    """process the request of signing in
    """
    session = package.get('session')
    params = package.get('params')
    username = params.get(ParamType.Username)
    password = params.get(ParamType.Password)
    user = UserHelper.get_user_by_username(username)
    if user is None:
        return Response.error_response('NoUser')
    if UserHelper.signin_check_password(user, password):
        EntryLogHelper.add_entrylog(session, user['id'])
        return Response.checked_response('SigninSuccess')
    return Response.error_response('PasswordError')

def verify_phone(package):
    """process the request of sending verify code
    """
    session = package.get('session')
    params = package.get('params')
    phone = params.get(ParamType.Phone)

    if not UserInfoChecker.check_phone(phone):
        return Response.error_response('IllegalPhone')

    lastcode = VerifyHelper.get_latest_code(session, phone)
    nowdate = getdate_now()
    if lastcode is not None and (nowdate.timestamp() - lastcode['time'].timestamp()) < 60:
        return Response.error_response('RequestTooFrequently')

    code = VerifyHelper.add_code(session, phone)
    if ConfigHelper.get_phone_verify_able():
        PhoneSender.send_verify_code(phone, code)
    else:
        EmailSender.send('chenxu17@mails.tsinghua.edu.cn', phone + '::' + code)
    return Response.checked_response('Success')

def signup(package):
    """process the request of signing up
    """
    session = package.get('session')
    params = package.get('params')
    username = params.get(ParamType.Username)
    password = params.get(ParamType.Password)
    phone = params.get(ParamType.Phone)
    verify_code = params.get(ParamType.CAPTCHA)

    if UserHelper.get_user_by_username(username) is not None:
        error_msg = 'Username exists'
    elif not VerifyHelper.check_code(session, phone, verify_code):
        error_msg = 'CAPTCHA Error'
    else:
        error_msg = None

    if error_msg is not None:
        return Response.error_response(error_msg)

    user_id = UserHelper.signup({
        'username' : username,
        'password' : password,
        'phone' : phone,
        'permission' : 1
    })
    user = UserHelper.get_user(user_id)
    if user is not None:
        EntryLogHelper.add_entrylog(session, user_id)
        return Response.checked_response('Signup Success')
    return Response.failed_response('System Error')

def signout(package):
    """process the request of signing out
    """
    session = package.get('session')
    EntryLogHelper.del_entrylog(session_id=session)
    return Response.checked_response("Logout")

def change_password(package):
    """process the request of changing password
    """
    session = package.get('session')
    params = package.get('params')
    oldpassword = params.get(ParamType.OldPassword)
    newpassword = params.get(ParamType.NewPassword)

    user = UserHelper.get_user_by_session(session)
    if user is None:
        return Response.error_response('No User')

    if not UserHelper.signin_check_password(user, oldpassword):
        return Response.error_response('Old Password Error')

    info = {
        'password' : newpassword
    }
    user_id = user.get('id')
    UserHelper.modify_user(user_id, info)

    return Response.success_response(None)
