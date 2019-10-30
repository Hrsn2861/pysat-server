"""views for school.school
"""
import utils.response as Response

from school.models import SchoolHelper
from utils.params import ParamType
from user.models import UserHelper

def create_school(package):
    """ Processing the request of creating a school
    """
    params = package.get('params')
    user_name = params.get(ParamType.UsernameWithDefault)
    school_name = params.get(ParamType.SchoolName)
    description = params.get(ParamType.Description)
    if user_name is None:
        user = package.get('user')
    else:
        user = UserHelper.get_user_by_username(user_name)
    if user is None:
        return Response.error_response("No User")
    if school_name is None:
        return Response.error_response("No School Name")
    school_id = SchoolHelper.add_school(user.id, school_name, description)
    return Response.success_response({'school_id' : school_id})
