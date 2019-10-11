from django.http import HttpResponse
import json

import server.model_utils.user as User
from server.posts.user_sign import user_verify


def user_list(request):

    result = None
    status = 0
    
    if request.method == 'GET':
        key = request.GET.get('key')
        page = str(request.GET.get("page"))
        if not page.isdigit():
            page = 1
        else:
            page = int(page)
        if page < 0:
            page = 1

        if request.GET.get("manager") is not None:
            manager = True
        else:
            manager = False

        me = user_verify(key)
        if me is None:
            status = 0
            msg = 'User login error.'
        else:
            result = {}
            result['count'] = User.user_count()
            result['list'] = User.user_list(page, manager, me['permission'] > 1)
            msg = 'Get.'
    else:
        status = -1
        msg = 'Invalid request'
    
    data = {
        'status': status,
        'msg': msg,
        'data': result
    }
    return HttpResponse(json.dumps(data))
