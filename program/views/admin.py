"""views for program.user
"""
import utils.response as Response
from utils.params import ParamType
from program.models import ProgramHelper
from user.models import PermissionHelper

def download(package):
    """process the request of downloading
    """
    user = package.get('user')
    user_id = user.get('id')
    params = package.get('params')
    program_id = (int)(params.get(ParamType.ProgramId))
    program = ProgramHelper.get_program(program_id)

    if program is None:
        return Response.error_response('No Program')

    prog_schoolid = program.get('schoolid')
    prog_status = program.get('status')

    if prog_status not in [0, 1, 2, 3]:
        return Response.error_response('Status not Valid')

    school_id = PermissionHelper.get_user_school(user_id)
    permission = PermissionHelper.get_permission(user_id, school_id)

    if permission > 4:
        if program.get('status') == 0:
            ProgramHelper.judging(program_id)
        info = {
            'content' : program['code'],
            'readme' : program['doc']
        }
        return Response.success_response({'code' : info})

    if prog_schoolid == 0:
        if user.get('permission') < 2:
            return Response.error_response('Access Denied')

    if school_id != prog_schoolid or permission < 2:
        return Response.error_response('Access Denied')

    if program.get('status') == 0:
        ProgramHelper.judging(program_id)

    info = {
        'content' : program['code'],
        'readme' : program['doc']
    }

    return Response.success_response({'code' : info})

def change_status(package):
    #pylint: disable-msg=too-many-return-statements
    #pylint: disable-msg=too-many-branches
    """proecess the request of change status
    """
    user = package.get('user')
    params = package.get('params')
    code_id = int(params.get(ParamType.ProgramId))
    source = int(params.get(ParamType.SourceStatus))
    target = int(params.get(ParamType.TargetStatus))

    check = (source, target)

    program = ProgramHelper.get_program(code_id)
    program_schoolid = program.get('schoolid')

    user_id = user.get('id')
    school_id = PermissionHelper.get_user_school(user_id)
    permission = PermissionHelper.get_permission(user_id, school_id)
    public_permission = user.get('permission')

    if permission > 4:
        if check not in [(0, 1), (1, 2), (1, -1), (2, 3), (3, 4), (4, 5)]:
            return Response.error_response('Cannot Change Status')
        if ProgramHelper.change_status(code_id, source, target) is False:
            return Response.error_response('Source Status Wrong')
        return Response.checked_response('Status Changed Successful')

    if program_schoolid == 0:
        if public_permission < 2:
            return Response.error_response('Access Denied')
        #如果是 在野审查员 不能上传
        if public_permission < 4:
            if check not in [(0, 1), (1, 2), (1, -1), (2, 3)]:
                return Response.error_response('Can\'t change status')
            if ProgramHelper.change_status(code_id, source, target) is False:
                return Response.error_response('Source Status Wrong')
            if check == (4, 5):
                ProgramHelper.upload(code_id)
            if check == (1, 2):
                ProgramHelper.judge_program(code_id, 2, user_id)
            return Response.checked_response('Status Changed Successful')
        #如果是 在野头目 则可以进行上传
        if check not in [(0, 1), (1, 2), (1, -1), (2, 3), (3, 4), (4, 5)]:
            return Response.error_response('Cannot Change Status')
        if ProgramHelper.change_status(code_id, source, target) is False:
            return Response.error_response('Source Status Wrong')
        if check == (4, 5):
            ProgramHelper.upload(code_id)
        if check == (1, 2):
            ProgramHelper.judge_program(code_id, 2, user_id)
        return Response.checked_response('Status Changed Successful')

    if school_id != program_schoolid:
        return Response.error_response('Access Denied: Not the same School')

    if permission < 2:
        return Response.error_response('Access Denied')
    if permission < 4:                      #如果只是普通管理员
        if check not in [(0, 1), (1, 2), (1, -1), (2, 3)]:
            return Response.error_response('Can\'t change status')
        if ProgramHelper.change_status(code_id, source, target) is False:
            return Response.error_response('Source Status Wrong')
        if check == (4, 5):
            ProgramHelper.upload(code_id)
        if check == (1, 2):
            ProgramHelper.judge_program(code_id, 2, user_id)
        return Response.checked_response('Status Changed Successful')

    if check not in [(0, 1), (1, 2), (1, -1), (2, 3), (3, 4), (4, 5)]:
        return Response.error_response('Cannot Change Status')
    if ProgramHelper.change_status(code_id, source, target) is False:
        return Response.error_response('Source Status Wrong')
    if check == (4, 5):
        ProgramHelper.upload(code_id)
    if check == (1, 2):
        ProgramHelper.judge_program(code_id, 2, user_id)
    return Response.checked_response('Status Changed Successful')
