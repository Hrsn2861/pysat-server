"""views for program.user
"""
import utils.response as Response
from utils.params import ParamType
from program.models import ProgramHelper

def upload(package):
    """process the request of uploading program
    """
    # user = package.get('user')
    params = package.get('params')
    program_id = int(params.get(ParamType.ProgramId))
    program = ProgramHelper.get_program(program_id)

    if program is None:
        return Response.error_response('No Program')

    if ProgramHelper.upload(program_id) is False:
        return Response.error_response('Upload Error')
    return Response.checked_response('Upload Success')

def judge(package):
    """process the request of judging program
    """
    user = package.get('user')
    params = package.get('params')
    program_id = int(params.get(ParamType.ProgramId)
)
    if ProgramHelper.judging(program_id, user.get('id')) is False:
        return Response.error_response('No Program')

    program_judge = (int)(params.get(ParamType.ProgramJudge))

    if program_judge == 1:
        status = 2
    elif program_judge == 0:
        status = -1
    else:
        return Response.error_response('Status Error')

    if ProgramHelper.judge_program(program_id, status, user.get('id')) is False:
        return Response.error_response('Judge Error')
    return Response.checked_response('Judge Success')

def download(package):
    """process the request of downloading
    """
    params = package.get('params')
    program_id = (int)(params.get(ParamType.ProgramId))
    program = ProgramHelper.get_program(program_id)

    if program is None:
        return Response.error_response('No Program')

    info = {
        'code' : program['code'],
        'readme' : program['doc']
    }

    return Response.success_response(info)
