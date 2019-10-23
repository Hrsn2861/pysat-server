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

    if listtype not in [0, 1, 2]:
        return Response.error_response('Invalid Listtype')

    page = params.get(ParamType.Page)

    if page is None or page == 0:
        page = 1
    progs_list = ProgramHelper.get_onstar_programs(page, listtype)

    if len(progs_list) == 0:
        return Response.checked_response('No Program')

    codelist = []
    for prog in progs_list:
        username = UserHelper.get_user(prog.get('id')).get('username')
        info = ProgramHelper.prog_filter(prog, username, True)
        codelist.append(info)

    data = {
        'tot_count' : ProgramHelper.get_programs_count({'status' : 3}),
        'now_count' : len(progs_list),
        'codelist' : codelist
    }

    return Response.success_response(data)

def mylist(package):
    """process the request of mylist
    """
    user = package.get('user')
    params = package.get('params')
    page = params.get(ParamType.Page)

    if page is None or page == 0:
        page = 1

    user_id = user.get('id')
    progs_list = ProgramHelper.get_user_programs(user_id, page, 0)

    if len(progs_list) == 0:
        return Response.checked_response('No Program')

    username = user.get('username')
    codelist = []
    for prog in progs_list:
        info = ProgramHelper.prog_filter(prog, username, False)
        codelist.append(info)

    data = {
        'tot_count' : ProgramHelper.get_user_programs_count(user_id),
        'now_count' : len(progs_list),
        'codelist' : codelist
    }

    return Response.success_response(data)

def inqueue_list(package):
    """All on star files
    """
    params = package.get('params')
    page = params.get(ParamType.Page)

    if page is None or page == 0:
        page = 1
    progs_list = ProgramHelper.get_inqueue_programs(page, 0)

    if len(progs_list) == 0:
        return Response.checked_response('No Program')

    codelist = []
    for prog in progs_list:
        username = UserHelper.get_user(prog.get('author')).get('username')
        info = ProgramHelper.prog_filter(prog, username, False)
        codelist.append(info)

    data = {
        'tot_count' : ProgramHelper.get_programs_count({'status' : 2}),
        'now_count' : len(progs_list),
        'codelist' : codelist
    }

    return Response.success_response(data)

def judge_list(package):
    """All on star files
    """
    params = package.get('params')
    page = params.get(ParamType.Page)

    if page is None or page == 0:
        page = 1
    progs_list = ProgramHelper.get_judge_programs(page, 0)

    if len(progs_list) == 0:
        return Response.checked_response('No Program')

    codelist = []
    for prog in progs_list:
        username = UserHelper.get_user(prog.get('author')).get('username')
        info = ProgramHelper.prog_filter(prog, username, False)
        info.update({'status' : prog.get('status')})
        codelist.append(info)

    data = {
        'tot_count' : ProgramHelper.get_programs_count({'status' : 0}),
        'now_count' : len(progs_list),
        'codelist' : codelist
    }

    return Response.success_response(data)
