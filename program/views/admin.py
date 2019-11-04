"""views for program.user
"""
import utils.response as Response
from utils.params import ParamType
from program.models import ProgramHelper
from user.models import PermissionHelper

def upload(package):
    """process the request of uploading program
    """
    # user = package.get('user')
    params = package.get('params')
    program_id = int(params.get(ParamType.ProgramId))
    program = ProgramHelper.get_program(program_id)

    if program is None:
        return Response.error_response('No Program')

    status = program.get('status')

    if status < 2:
        return Response.error_response('Program did not pass audit')

    if ProgramHelper.upload(program_id) is False:
        return Response.error_response('Upload Error')
    return Response.checked_response('Upload Success')

def judge(package):
    """process the request of judging program
    """
    user = package.get('user')
    params = package.get('params')
    program_id = int(params.get(ParamType.ProgramId))
    program_judge = (int)(params.get(ParamType.ProgramJudge))

    program = ProgramHelper.get_program(program_id)
    if program.get('status') != 1:
        return Response.checked_response('Status is not judging')

    if program_judge == 1:
        status = 2
    elif program_judge == 0:
        status = -1
    else:
        return Response.error_response('Judge Status Error')

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

    if program.get('status') == 0:
        ProgramHelper.judging(program_id)

    info = {
        'content' : program['code'],
        'readme' : program['doc']
    }

    return Response.success_response({'code' : info})

def change_status(package):
    """proecess the request of change status
    """
    user = package.get('user')
    params = package.get('params')
    code_id = int(params.get(ParamType.ProgramId))
    source = int(params.get(ParamType.SourceStatus))
    target = int(params.get(ParamType.TargetStatus))

    check = (source, target)

    user_id = user.get('id')
    school_id = PermissionHelper.get_user_school(user_id)
    permission = PermissionHelper.get_permission(user_id, school_id)

    if permission < 4:                      #如果只是普通管理员
        if check not in [(0, 1), (1, 2), (1, -1), (2, 3)]:
            return Response.error_response('Can\'t change status')
        if ProgramHelper.change_status(code_id, source, target) is False:
            return Response.error_response('Source Status Wrong')
        return Response.checked_response('Status Changed Successful')

    if check not in [(0, 1), (1, 2), (1, -1), (2, 3), (3, 4), (4, 5)]:
        return Response.error_response('Cannot Change Status')
    if ProgramHelper.change_status(code_id, source, target) is False:
        return Response.error_response('Source Status Wrong')
    return Response.checked_response('Status Changed Successful')
