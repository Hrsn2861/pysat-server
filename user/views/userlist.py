"""views for user.list
"""
import utils.response as Response

from utils.params import ParamType
from user.models import UserHelper, PermissionHelper
from program.models import ProgramHelper

def getlist(package):
    #pylint: disable-msg=too-many-locals
    """process the request of getting user's info
    """
    params = package.get('params')
    show_invalid = params.get(ParamType.ShowInvalid) == 'true'
    manager_first = params.get(ParamType.ManagerFirst) == 'true'
    school_id = int(params.get(ParamType.SchoolId))
    page = params.get(ParamType.Page)

    if page is None:
        page = 1
    page = int(page)

    if school_id == 0:
        user_list = UserHelper.user_list(page, show_invalid, manager_first)
        ret_list = []
        if len(user_list) == 0:
            data = {
                'tot_count' : UserHelper.user_count(show_invalid),
                'now_count' : 0,
                'user_list' : []
            }
            return Response.success_response(data)

        for user in user_list:
            download = ProgramHelper.count_user_downloadlog(user.get('id'))
            ret_list.append({
                'username' : user.get('username'),
                'motto' : user.get('motto'),
                'permission' : user.get('permission'),
                'download' : download
            })
            data = {
                'tot_count' : UserHelper.user_count(show_invalid),
                'now_count' : len(ret_list),
                'user_list' : ret_list
            }
        return Response.success_response(data)

    buf_userlist = UserHelper.get_all(
        show_invalid, manager_first
    )
    userlist = []

    for user in buf_userlist:
        user_id = user.get('id')
        school = PermissionHelper.get_user_school(user_id)
        if school_id != school:
            continue
        download = ProgramHelper.count_user_downloadlog(user.get('id'))
        permission_private = PermissionHelper.get_permission(user_id, school)
        print('permission private', permission_private)
        userlist.append({
            'username' : user['username'],
            'motto' : user['motto'],
            'permission' : permission_private,
            'download' : download
        })
    if len(userlist) < (page-1) * 20:
        data = {
            'tot_count' : len(userlist),
            'now_count' : 0,
            'user_list' : []
        }
        return Response.success_response(data)
    pagelist = userlist[(page - 1) * 20 : page * 20]
    data = {
        'tot_count' : len(userlist),
        'now_count' : len(pagelist),
        'user_list' : userlist,
    }
    return Response.success_response(data)
