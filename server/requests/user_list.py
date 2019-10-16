"""requests: user/list
"""

from django.views.decorators.csrf import csrf_exempt

import server.utils.models.user as User
import server.utils.models.session as Session
import server.utils.response as Response

from server.utils.params import check_params, ParamType
from server.utils.request import get_ip

@csrf_exempt
def user_list_get(request):
    """process the request of getting user's info
    """
    if request.method == 'GET':
        ip_address = get_ip(request)

        token = request.GET.get('token')
        show_invalid = request.GET.get('show_invalid')
        manager_first = request.GET.get('manager_first')
        page = request.GET.get('page')

        if page is None:
            page = 1

        error = check_params({
            ParamType.Token : token,
            ParamType.ShowInvalidForUserList : show_invalid,
            ParamType.ManagerFirstForUserList : manager_first,
            ParamType.PageForUserList : page
        })
        if error is not None:
            return error

        session_id = Session.get_session_id(token, ip_address)
        if session_id is None:
            return Response.error_response("NoSession")

        buf_userlist = User.user_list(page, show_invalid, manager_first)

        userlist = []

        for user in buf_userlist:
            userlist.append({
                'username' : user['username'],
                'motto' : user['motto'],
                'permission' : user['permission']
            })

        data = {
            'tot_count' : User.user_count(show_invalid),
            'now_count' : len(userlist),
            'userlist' : userlist,
        }

        if buf_userlist or buf_userlist is None:
            return Response.error_response("NoUser")
        return Response.success_response(data)
    return Response.invalid_request()
