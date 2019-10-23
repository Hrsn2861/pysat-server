"""views for user.list
"""
import utils.response as Response

from utils.params import ParamType
from user.models import UserHelper

def getlist(package):
    """process the request of getting user's info
    """
    params = package.get('params')
    show_invalid = params.get(ParamType.ShowInvalid) == 'true'
    manager_first = params.get(ParamType.ManagerFirst) == 'true'
    page = params.get(ParamType.Page)

    if page is None:
        page = 1
    page = int(page)

    buf_userlist = UserHelper.user_list(page, show_invalid, manager_first)
    userlist = []
    for user in buf_userlist:
        userlist.append({
            'username' : user['username'],
            'motto' : user['motto'],
            'permission' : user['permission']
        })
    data = {
        'tot_count' : UserHelper.user_count(show_invalid),
        'now_count' : len(userlist),
        'userlist' : userlist,
    }
    return Response.success_response(data)
