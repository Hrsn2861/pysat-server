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
