"""views for program.list
"""
import utils.response as Response
from utils.params import ParamType
from program.models import ProgramHelper
from user.models import UserHelper

def onstar_list(package):
    """All on star files
    """
    params = package.get('params')
    listtype = (int)(params.get(ParamType.Listype))

    if listtype not in [0,1,2]:
        return Response.error_response('Invalid Listtype')

    page = params.get(ParamType.Page)

    if page is None or page == 0:
        page = 1
    progs_list = ProgramHelper.get_onstar_programs(page, listtype)

    if progs_list is None:
        return Response.checked_response('No Programs')

    codelist = []
    for prog in progs_list:
        info = {
            'id' : prog.get('id'),
            'name' : prog.get('name'),
            'author' : UserHelper.get_user(prog.get('id')).get('username'),
            'downloads' : prog.get('downloads'),
            'likes' : prog.get('likes'),
            'upload_time' : prog.get('upload_time')
        }
        codelist.append(info)

    data = {
        'tot_count' : ProgramHelper.get_programs_count({'status' : 3}),
        'now_count' : len(progs_list),
        'codelist' : codelist
    }

    return Response.success_response(data)
