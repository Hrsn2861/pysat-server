"""views for program.user
"""
import utils.response as Response
from utils.params import ParamType
from program.models import ProgramHelper
from program.models import ProgramLikeHelper

def submit(package):
    """process the request of submitting program
    """
    user = package.get('user')
    params = package.get('params')
    program_name = params.get(ParamType.ProgramName)
    program_code = params.get(ParamType.ProgramCode)
    program_doc = params.get(ParamType.ProgramDoc)
    ProgramHelper.add_program(user['id'], program_name, program_code, program_doc)
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

    user_id = user.get('id')
    ProgramLikeHelper.add_like(user_id, prog_id)
    ProgramHelper.like_program(prog_id)

    # program = ProgramHelper.get_program(prog_id)
    # return Response.checked_response(str(program.get('likes')))

    return Response.checked_response('Like Successful')
