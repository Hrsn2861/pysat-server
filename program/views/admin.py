"""views for program.user
"""
import utils.response as Response
from utils.params import ParamType
from program.models import ProgramHelper

def upload(package):
    """process the request of uploading program
    """
    user = package.get('user')
    params = package.get('params')
    program_id = params.get(ParamType.ProgramId)
    program = ProgramHelper.get_program(program_id)

    if program is None:
        return Response.error_response('No Program')
    program_name = program['name']
    program_code = program['code']
    program_doc = program['doc']

    ProgramHelper.add_program(user['id'], program_name, program_code, program_doc)
    return Response.checked_response('Upload Success')
