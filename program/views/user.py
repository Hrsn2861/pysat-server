"""views for program.user
"""
import utils.response as Response
from utils.params import ParamType
from program.models import ProgramHelper

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
