"""views for school.user
"""
import utils.response as Response

from utils.params import ParamType
from school.models import SchoolHelper
from school.models import SchoolApplyHelper

def apply_for_school(package):
    """ Processing the request of applying for school
    """
    params = package.get('params')
    user = package.get('user')
    if user is None:
        return Response.error_response('No User')
    apply_message = params.get(ParamType.ApplyMessage)
    if apply_message is None:
        return Response.error_response('No Apply Message')
    school_name = params.get(ParamType.SchoolName)
    if SchoolHelper.get_school_count(school_name) > 1:
        return Response.error_response('Multiple Schools')
    if SchoolHelper.get_school_count(school_name) < 1:
        return Response.error_response('No School')
    school = SchoolHelper.get_school_list(1, school_name)[0]
    if SchoolApplyHelper.add_apply(user.id, school.id, apply_message) is True:
        return Response.success_response(None)
    return Response.error_response('Apply Failed')
