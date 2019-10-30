"""views maker
"""
import utils.response as Response

from utils.params import check_params, ParamType
from utils.checker import UserInfoChecker
from utils.request import get_ip
from utils.cipher import decrypt
from utils.permission import PermissionManager

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

def view_maker(func, method, paramlist=None, checklist=None, action=None):
    """view maker
    """

    def method_check(package):
        request = package['request']
        error = None
        if request.method != package['method']:
            error = Response.invalid_request()
        return package, error

    def param_check(package):
        request = package['request']
        paramlist = package['paramlist']
        if paramlist is None:
            paramlist = list()
        if func is not start_session:
            paramlist.insert(0, ParamType.Token)
        if method == 'POST':
            params = paramlist_to_params(request.POST, paramlist)
        else:
            params = paramlist_to_params(request.GET, paramlist)
        package['params'] = params
        return package, check_params(params)

    def session_check(package):
        params = package['params']
        ip_address = package['ip']
        session = SessionHelper.get_session_id(params[ParamType.Token], ip_address)
        error = None
        if session is None:
            error = Response.error_response('No Session')
        else:
            package['session'] = session
            package['user'] = UserHelper.get_user_by_session(session)
        return package, error

    def info_check(package):
        params = package['params']
        checklist = package['checklist']
        error = UserInfoChecker.check(checklist_to_checks(params, checklist))
        return package, error

    def action_check(package):
        user = package['user']
        action = package['action']
        error = None
        if not PermissionManager.check_user(user, action):
            error = Response.error_response('Access Denied')
        return package, error

    checks = [method_check, param_check, session_check]
    if checklist is not None:
        checks.append(info_check)
    if action is not None:
        checks.append(action_check)

    def basic_view(request):
        """basic view
        """
        ip_address = get_ip(request)
        if func is not start_session:
            package = {
                'request' : request,
                'ip' : ip_address,
                'method' : method,
                'paramlist' : paramlist,
                'checklist' : checklist,
                'action' : action,
                'file' : request.FILES.get('file', None)
            }
            for check in checks:
                package, error = check(package)
                if error is not None:
                    return error
            return func(package)
        token = SessionHelper.add_session(ip_address)
        return Response.success_response(data={'token' : token})

    return basic_view
