"""views maker
"""
import utils.response as Response

from utils.params import check_params, ParamType
from utils.checker import UserInfoChecker
from utils.request import get_ip
from utils.cipher import decrypt

from session.models import SessionHelper
from session.views import start_session

from user.models import UserHelper

def paramlist_to_params(paramsrc, paramlist):
    """special function for `view_base`

    it can transform paramlist into params
    """
    params = {}
    for param in paramlist:
        _, key, encrypted, _, _, _ = param.value
        value = paramsrc.get(key)
        if encrypted:
            value = decrypt(value)
        params[param] = value
    return params

def checklist_to_checks(params, checklist):
    """special function for `view_base`

    it can transform checklist into checks
    """
    checks = {}
    for check_param in checklist:
        if check_param in params:
            _, _, _, _, _, check_type = check_param.value
            checks[check_type] = params[check_param]
    return checks


def view_base(request, func, method, paramlist, checklist):
    """basic view
    """
    if method not in ['POST', 'GET']:
        return Response.failed_response('System Error (Unknown `method` for request.method)')
    check_token = func is not start_session
    if request.method == method:
        ip_address = get_ip(request)
        if check_token:
            paramlist.insert(0, ParamType.Token)
        if method == 'POST':
            params = paramlist_to_params(request.POST, paramlist)
        else:
            params = paramlist_to_params(request.GET, paramlist)
        error_msg = check_params(params)
        if error_msg is None:
            error_msg = UserInfoChecker.check(checklist_to_checks(params, checklist))
        if error_msg is not None:
            return error_msg
        if check_token:
            session = SessionHelper.get_session_id(params[ParamType.Token], ip_address)
            if session is None:
                return Response.error_response("No Session")
            return func({
                'request' : request,
                'ip' : ip_address,
                'session' : session,
                'user' : UserHelper.get_user_by_session(session),
                'params' : params
            })
        return Response.success_response(data={'token' : SessionHelper.add_session(ip_address)})
    return Response.invalid_request()

def view_maker(func, method, paramlist=None, checklist=None):
    """view maker

    return a function
    """
    if paramlist is None:
        paramlist = list()
    if checklist is None:
        checklist = list()
    return lambda request: view_base(request, func, method, paramlist, checklist)
