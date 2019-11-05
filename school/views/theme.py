"""views for school.theme
"""
import utils.response as Response

from school.models import SubjectHelper
from program.models import ProgramHelper
from utils.params import ParamType
from user.models import PermissionHelper

def create_theme(package):
    """create a theme
    """
    user = package.get('user')
    params = package.get('params')
    target_schoolid = params.get(ParamType.SchoolIdWithDefault)
    name = params.get(ParamType.ThemeName)
    msg = params.get(ParamType.ThemeDescription)
    deadline = params.get(ParamType.ThemeDeadline)

    userid = user.get('id')
    school_id = PermissionHelper.get_user_school(userid)
    private_permission = PermissionHelper.get_permission(userid, school_id)
    public_permission = user['permission']

    if public_permission > 1 and private_permission > 1:
        if target_schoolid is None:
            return Response.error_response('Invalid SchoolId')
        target_schoolid = (int)(target_schoolid)
        SubjectHelper.add_subject(target_schoolid, name, msg, deadline)
        return Response.checked_response('Create Successful')

    if public_permission > 1:
        SubjectHelper.add_subject(0, name, msg, deadline)
        return Response.checked_response('Create Successful')

    SubjectHelper.add_subject(school_id, name, msg, deadline)
    return Response.checked_response('Create Successful')

def get_list(package):
    """get theme list
    """
    user = package.get('user')
    params = package.get('params')
    target_schoolid = int(params.get(ParamType.SchoolId))
    page = params.get(ParamType.Page)

    if page is None:
        page = 1
    page = int(page)

    user_id = user.get('id')
    school_id = PermissionHelper.get_user_school(user_id)
    public_permission = user.get('permission')

    if target_schoolid != 0:
        if target_schoolid != school_id and public_permission < 8:
            return Response.error_response('Access Denied')

    theme_list = SubjectHelper.get_subjects(
        target_schoolid, 0, page
    )

    for theme in theme_list:
        theme.update({
            'count' : ProgramHelper.get_subject_programs_count(theme.get('id'))
        })
    ret = {
        'tot_count' : SubjectHelper.get_subject_count(target_schoolid, 0),
        'now_count' : len(theme_list),
        'theme_list' : theme_list
    }

    return Response.success_response(ret)

def delete_theme(package):
    """delete theme
    """
    user = package.get('user')
    user_id = user.get('id')
    school_id = PermissionHelper.get_user_school(user_id)

    params = package.get('params')
    theme_id = int(params.get(ParamType.ThemeId))

    theme = SubjectHelper.get_subject_with_schoolid(theme_id)
    if theme is None:
        return Response.error_response('No Subject')
    theme_schoolid = theme.get('school_id')

    private_permission = PermissionHelper.get_permission(user_id, school_id)

    if private_permission < 4:                                  #非高级管理员
        return Response.error_response('Access Denied')

    if private_permission < 8:                                  #非超级用户
        if school_id != theme_schoolid:                         #学校必须匹配
            return Response.error_response('Acess Denied')
    SubjectHelper.delete_subject(theme_id)
    return Response.checked_response('Delete Success')

def modify_theme(package):
    """modify theme
    """
    user = package.get('user')
    user_id = user.get('id')
    school_id = PermissionHelper.get_user_school(user_id)

    params = package.get('params')
    theme_id = int(params.get(ParamType.ThemeId))
    title = params.get(ParamType.ThemeNameWithDefault)
    description = params.get(ParamType.ThemeDescriptionWithDefault)
    deadline = params.get(ParamType.ThemeDeadlineWithDefault)

    theme = SubjectHelper.get_subject_with_schoolid(theme_id)
    if theme is None:
        return Response.error_response('No Subject')
    theme_schoolid = theme.get('school_id')

    private_permission = PermissionHelper.get_permission(user_id, school_id)

    if private_permission < 4:                                  #非高级管理员
        return Response.error_response('Access Denied')

    if private_permission < 8:                                  #非超级用户
        if school_id != theme_schoolid:                         #学校必须匹配
            return Response.error_response('Acess Denied')

    SubjectHelper.mofidy_subject(theme_id, title, description, deadline)
    return Response.checked_response('Modify Success')
