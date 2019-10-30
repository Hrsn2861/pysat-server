"""views for user.info
"""
import utils.response as Response

from utils.params import ParamType
from school.models import SchoolHelper

def create_school(package):
    """ Processing the request of creating a school
    """
    params = package.get('params')
    user_id = params.get(ParamType.Id)
    school_name = params.get(ParamType.SchoolForCreate)
    school_description = params.get(ParamType.SchoolDescription)
    if user_id is None:
        return Response.error_response("No User ID")
    if school_name is None:
        return Response.error_response("No School Name")
    school_id = SchoolHelper.add_school(user_id, school_name, school_description)
    return Response.success_response({'school_id' : school_id})
