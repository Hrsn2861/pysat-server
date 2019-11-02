"""views for program.list
"""
import utils.response as Response
from utils.params import ParamType
from program.models import ProgramHelper
from program.models import ProgramLikeHelper
from program.models import DownloadLogHelper

from user.models import UserHelper

def get_program_list(package):
    #pylint: disable-msg=too-many-locals
    #pylint: disable-msg=too-many-return-statements
    #pylint: disable-msg=too-many-branches
    #pylint: disable-msg=too-many-statements
    """All list
    """
    params = package.get('params')
    user = package.get('user')
    mine = params.get(ParamType.Mine)
    schoolid = params.get(ParamType.School)
    status_up = params.get(ParamType.StatusUp)
    status_low = params.get(ParamType.StatusDown)
    subjectid = params.get(ParamType.Theme)
    listtype = params.get(ParamType.Listype)
    page = params.get(ParamType.Page)

    if schoolid is not None:
        schoolid = int(schoolid)
    if subjectid is not None:
        subjectid = int(subjectid)
    if status_up is not None:
        status_up = int(status_up)
    else:
        status_up = 6
    if status_low is not None:
        status_low = int(status_low)
    else:
        status_low = -3
    if listtype is not None:
        listtype = int(listtype)
    else:
        listtype = 0

    if page is None:
        page = 1
    else:
        page = int(page)

    if status_up not in range(-4, 7):
        return Response.error_response('Illegel Status Upper Limit')
    if status_low not in range(-4, 7):
        return Response.error_response('Illegal Status Lower Limit')

    if mine == 'true':
        user_id = user.get('id')
        progs_list = ProgramHelper.get_user_programs(user_id, page, listtype)

        if len(progs_list) == 0:
            data = {
                'tot_count' : 0,
                'now_count' : 0,
                'codelist' : []
            }
            return Response.success_response(data)

        username = user.get('username')
        codelist = []
        for prog in progs_list:
            prog_id = prog.get('id')
            liked = ProgramLikeHelper.check_like(user_id, prog_id)
            downloaded = DownloadLogHelper.check_download(user_id, prog_id)
            info = ProgramHelper.prog_filter(
                prog, username, downloaded, liked
                )
            codelist.append(info)

        data = {
            'tot_count' : ProgramHelper.get_user_programs_count(user_id),
            'now_count' : len(progs_list),
            'codelist' : codelist
        }

        return Response.success_response(data)

    if schoolid is None:
        return Response.error_response('Invalid School')

    user_id = user.get('id')
    progs_list = ProgramHelper.get_programs_school(
        status_up, status_low, schoolid, subjectid, page, listtype
        )

    if len(progs_list) == 0:
        data = {
            'tot_count' : 0,
            'now_count' : 0,
            'codelist' : []
        }
        return Response.success_response(data)

    username = user.get('username')
    codelist = []

    for prog in progs_list:
        prog_id = prog.get('id')
        liked = ProgramLikeHelper.check_like(user_id, prog_id)
        downloaded = DownloadLogHelper.check_download(user_id, prog_id)
        info = ProgramHelper.prog_filter(
            prog, username, downloaded, liked
            )
        codelist.append(info)
    data = {
        'tot_count' : ProgramHelper.get_programs_school_count(
            status_up, status_low, schoolid, subjectid
        ),
        'now_count' : len(progs_list),
        'codelist' : codelist
    }
    return Response.success_response(data)
