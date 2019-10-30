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
    schoolid = params.get(ParamType.SchoolIdWithoutDefault)

    school = SchoolHelper.get_school(schoolid)

    if school is None:
        return Response.error_response('No School Found')
    SchoolApplyHelper.add_apply(user.get('id'), schoolid, apply_message)
    return Response.checked_response('Applied Successed')
