"""views for program.user
"""
import utils.response as Response
from utils.params import ParamType
from program.models import ProgramHelper
from program.models import ProgramLikeHelper
from program.models import DownloadLogHelper

def submit(package):
    """process the request of submitting program
    """
    user = package.get('user')
    params = package.get('params')
    program_name = params.get(ParamType.ProgramName)
    program_code = params.get(ParamType.ProgramCode)
    program_doc = params.get(ParamType.ProgramDoc)
    program_school = int(params.get(ParamType.Schoolid))
    program_subject = int(params.get(ParamType.Theme))
    ProgramHelper.add_program(
        user['id'], program_name, program_code,
        program_doc, program_school, program_subject
        )
    return Response.checked_response('Submit Success')

def like(package):
    """process the request of like program
    """
    user = package.get('user')
    params = package.get('params')
    prog_id = (int)(params.get(ParamType.ProgramId))
    program = ProgramHelper.get_program(prog_id)

    if program is None:
        return Response.error_response('No Program')

    if program.get('status') != 3:
        return Response.error_response('Program not valid')

    user_id = user.get('id')

    if ProgramLikeHelper.check_like(user_id, prog_id):
        return Response.checked_response('User liked before')

    ProgramLikeHelper.add_like(user_id, prog_id)
    like_count = ProgramLikeHelper.count_like(prog_id)
    ProgramHelper.set_likes(prog_id, like_count)

    # program = ProgramHelper.get_program(prog_id)
    # return Response.checked_response(str(program.get('likes')))

    return Response.checked_response('Like Successful')

def download(package):
    """user download program
    """
    user = package.get('user')
    params = package.get('params')
    prog_id = (int)(params.get(ParamType.ProgramId))
    user_id = user.get('id')

    program = ProgramHelper.get_program(prog_id)

    if program is None:
        return Response.error_response('No Program')

    if not DownloadLogHelper.check_download(user_id, prog_id):
        DownloadLogHelper.add_downloadlog(user_id, prog_id)
        log_count = DownloadLogHelper.count_downloadlog(prog_id)
        ProgramHelper.set_downloads(prog_id, log_count)

    info = {
        'code' : program.get('code'),
        'readme' : program.get('doc')
    }

    # program = ProgramHelper.get_program(prog_id)
    # return Response.checked_response(str(program.get('downloads')))

    return Response.success_response(info)
