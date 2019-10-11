"""requests: user/sign
"""

from django.views.decorators.csrf import csrf_exempt

import server.utils.response as Response
import server.utils.models.user as User
import server.utils.models.session as Session
import server.utils.models.entrylog as EntryLog
import server.utils.models.config as Config
import server.utils.models.verifycode as VerufyCode

import server.utils.code_sender.phone as PhoneSender
import server.utils.code_sender.email as EmailSender

from server.utils.params import check_params, ParamType
from server.utils.cipher import decrypt
from server.utils.request import get_ip
from server.utils.utils import getdate_now

@csrf_exempt
def signin(request):
    """process the request of signing in
    """
    if request.method == 'POST':
        ip_address = get_ip(request)

        token = request.POST.get('token')
        username = request.POST.get('username')
        password = request.POST.get('password')
        password = decrypt(password)

        error = check_params({
            ParamType.Token : token,
            ParamType.Username : username,
            ParamType.Password : password
        })
        if error is not None:
            return error

        session_id = Session.get_session_id(token, ip_address)
        if session_id is None:
            return Response.error_response("NoSession")

        user = User.get_user_by_username(username)
        if user is None:
            return Response.error_response("NoUser")
        if User.signin_check_password(user, password):
            EntryLog.add_entrylog(session_id, user['id'])
            return Response.checked_response("SigninSuccess")
        return Response.error_response("PasswordError")
    return Response.invalid_request()


@csrf_exempt
def verify_phone(request):
    """verify phone
    """
    if request.method == 'POST':
        ip_address = get_ip(request)

        token = request.POST.get('token')
        phone = request.POST.get('phone')

        error = check_params({
            ParamType.Token : token,
            ParamType.Phone : phone
        })
        if error is not None:
            return error

        session_id = Session.get_session_id(token, ip_address)
        if session_id is None:
            return Response.error_response("NoSession")

        if not User.UserInfoChecker.check_phone(phone):
            return Response.error_response("IllegalPhone")

        lastcode = VerufyCode.get_latest_code(session_id, phone)
        nowdate = getdate_now()
        if lastcode is not None and (nowdate.timestamp() - lastcode['time'].timestamp()) < 60:
            return Response.error_response("RequestTooFrequently")

        code = VerufyCode.add_code(session_id, phone)
        if Config.get_phone_verify_able():
            PhoneSender.send_verify_code(phone, code)
        else:
            EmailSender.send("chenxu17@mails.tsinghua.edu.cn", phone + "::" + code)
        return Response.checked_response("Success")
    return Response.invalid_request()


@csrf_exempt
def signup(request):
    """process the request of signing up
    """
    if request.method == 'POST':
        ip_address = get_ip(request)

        token = request.POST.get('token')
        username = request.POST.get('username')
        password = request.POST.get('password')
        password = decrypt(password)
        phone = request.POST.get('phone')
        verify_code = request.POST.get('CAPTCHA')

        error = check_params({
            ParamType.Token : token,
            ParamType.Username : username,
            ParamType.Password : password,
            ParamType.Phone : phone,
            ParamType.CAPTCHA : verify_code
        })
        if error is None:
            error = User.UserInfoChecker.check({
                (User.UserInfoChecker.check_username, "Username") : username,
                (User.UserInfoChecker.check_phone, "Phone") : phone,
                (User.UserInfoChecker.check_password, "Password") : password
            })
        if error is not None:
            return error

        session_id = Session.get_session_id(token, ip_address)
        if session_id is None:
            error_msg = "NoSession"
        elif User.get_user_by_username(username) is not None:
            error_msg = "DuplicateUsername"
        elif not VerufyCode.check_code(session_id, phone, verify_code):
            error_msg = "CAPTCHA Error"
        else:
            error_msg = None

        if error_msg is not None:
            return Response.error_response(error_msg)

        user_id = User.signup({
            'username' : username,
            'password' : password,
            'phone' : phone,
            'permission' : 1
        })
        user = User.get_user(user_id)
        if user is not None:
            EntryLog.add_entrylog(session_id, user_id)
            return Response.checked_response("SignupSuccess")
        return Response.failed_response("UnknownError")
    return Response.invalid_request()


@csrf_exempt
def signout(request):
    """process the request of signing out
    """
    if request.method == 'POST':
        ip_address = get_ip(request)

        token = request.POST.get('token')
        error = check_params({
            ParamType.Token : token
        })
        if error is not None:
            return error

        session_id = Session.get_session_id(token, ip_address)
        if session_id is None:
            return Response.error_response("NoSession")

        EntryLog.del_entrylog(session_id=session_id)
        return Response.checked_response("Logout")
    return Response.invalid_request()
