"""views for school.school
"""
import utils.response as Response

from utils.params import ParamType
from school.models import SchoolHelper
from user.models import UserHelper

def create_school(package):
    """ Processing the request of creating a school
    """
    user = package.get('user')
    creator_id = user.get('id')

    params = package.get('params')
    user_name = params.get(ParamType.Username)
    school_name = params.get(ParamType.SchoolName)
    description = params.get(ParamType.SchoolDescription)

    headmaster = UserHelper.get_user_by_username(user_name)

    if headmaster is None:
        return Response.error_response("No User")

    if SchoolHelper.get_school_by_name(school_name) is not None:
        return Response.error_response('School Exist')

    SchoolHelper.add_school(creator_id, school_name, description, headmaster.get('id'))
    return Response.checked_response('Create Succeessful')

def get_school_list(package):
    """ Processing the request of getting school list
    """
    params = package.get('params')
    page = params.get(ParamType.Page)
    search_text = params.get(ParamType.SearchText)
    if page is None:
        page = 1
    page = int(page)
    if int(page) < 1:
        return Response.error_response('Invalid Page Number')

    school_list = SchoolHelper.get_school_list(page, search_text)

    for school in school_list:
        buf_name = school.get('schoolname')
        del school['schoolname']
        school.update({
            'name' : buf_name
        })

    tot_count = SchoolHelper.get_school_count(search_text)
    return Response.success_response({
        'tot_count' : tot_count,
        'now_count' : len(school_list),
        'school_list' : school_list
        })
