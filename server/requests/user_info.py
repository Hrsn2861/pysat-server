"""requests: user/info
"""

from django.views.decorators.csrf import csrf_exempt

import server.utils.models.user as User
import server.utils.models.session as Session
import server.utils.response as Response

from server.utils.params import check_params, ParamType
from server.utils.request import get_ip

@csrf_exempt
def get_info(request):
    """process the request of getting user's info
    """
    if request.method == 'GET':
        ip_address = get_ip(request)

        token = request.GET.get('token')
        username = request.GET.get('username')

        error = check_params({
            ParamType.Token : token,
            ParamType.UsernameForInfo : username
        })
        if error is not None:
            return error

        session_id = Session.get_session_id(token, ip_address)
        if session_id is None:
            return Response.error_response("NoSession")

        if username is None:
            user = User.get_user_by_session(session_id)
        else:
            user = User.get_user_by_username(username)
        if user is None:
            return Response.error_response("NoUser")
        user = User.user_filter(user)
        return Response.success_response({'user' : user})
    return Response.invalid_request()

@csrf_exempt
def modify_info(request):
    """Process the request of modyfying user's info
    """
    if request.method == 'POST':
        ip_address = get_ip(request)

        token = request.POST.get('token')
        username = request.POST.get('username')
        realname = request.POST.get('realname')
        school = request.POST.get('school')
        motto = request.POST.get('motto')
        permission = request.POST.get('permission')

        session_id = Session.get_session_id(token, ip_address)
        if session_id is None:
            return Response.error_response("NoSession")
        
        if username is None:
            user = User.get_user_by_session(session_id)
        else:
            user = User.get_user_by_username(username)

        # test
        # user = {
        #     "username" : 'test',
        #     'realname' : 'realname',
        #     'school' : 'tsinghua',
        #     'motto' : 'I am stupid.',
        #     'permission' : "1"
        # }
        
        if user is None:
            return Response.error_response("NoUser")
        user = User.user_filter(user)

        if realname is None:
            realname = user.get("realname")
        if school is None:
            school = user.get("school")
        if motto is None:
            motto = user.get("motto")
        if permission is None:
            permission = user.get("permission")

        error = User.UserInfoChecker.check({
            (User.UserInfoChecker.check_realname, "Realname") : realname,
            (User.UserInfoChecker.check_school, "School") : school
        })

        if error is not None:
            return error

        error = check_params({
            ParamType.Token : token,
            ParamType.ModifyUsername : username,
            ParamType.ModifyRealname : realname,
            ParamType.ModifySchool : school,
            ParamType.ModifyMotto : motto,
            ParamType.ModifyPermission : permission
        })

        if error is not None:
            return error

        info = {
            "realname" : realname,
            "school" : school,
            "motto" : motto,
            "permission" : permission
        }
        User.modify_user(user.get('id'), info)

        return Response.success_response(None)
    else:
        return Response.invalid_request()

