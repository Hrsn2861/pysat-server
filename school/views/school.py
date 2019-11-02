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

    school_id = SchoolHelper.add_school(user.get('id'), school_name, description)
    return Response.success_response({'school_id' : school_id})

def get_school_list(package):
    """ Processing the request of getting school list
    """
    params = package.get('params')
    page = params.get(ParamType.Page)
    search_text = params.get(ParamType.SearchText)
    if page is None:
        page = 1
    if page < 0:
        return Response.error_response('Invalid Page Number')
    
    school_list = SchoolHelper.get_school_list(page, search_text)
    tot_count = SchoolHelper.get_school_count(search_text)
    return Response.success_response({
        'tot_count' : tot_count,
        'now_count' : len(school_list),
        'school_list' : school_list
        })
