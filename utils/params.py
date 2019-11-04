"""check params for request
"""

from enum import Enum
import utils.response as Response

from utils.checker import UserInfoType

def check_str_as_bool(value):
    """check `value` if it's boolean
    """
    value = value.lower()
    if value in ['true', 'false']:
        return True
    return False

def check_str_as_int(value):
    """check `value` if it's integer
    """
    try:
        value = int(value)
        return isinstance(value, int)
    except ValueError:
        return False

def check_params(params):
    """check params for request
    """
    for key, value in params.items():
        name, _, _, need, param_type, _ = key.value
        if param_type not in ['string', 'integer', 'boolean']:
            return Response.failed_response('System Error (Unkown param type)')

        if need is True and value is None:
            return Response.error_response('Invalid ' + name)
        if value is not None:
            if param_type == 'boolean' and check_str_as_bool(value) is False:
                return Response.error_response('Invalid ' + name)
            if param_type == 'integer' and check_str_as_int(value) is False:
                return Response.error_response('Invalid ' + name)
    return None

class ParamType(Enum):
    """params for requests

    ParamType.Key = ('param name', 'param key', encrypted, notnull, type, type_for_check)
    """
    Token = ('Token', 'token', False, True, 'string', UserInfoType.Pass)

    Username = ('Username', 'username', False, True, 'string', UserInfoType.Username)
    UsernameWithDefault = ('Username', 'username', False, False, 'string', UserInfoType.Username)

    Password = ('Password', 'password', True, True, 'string', UserInfoType.Password)
    OldPassword = ('Old Password', 'oldpassword', True, True, 'string', UserInfoType.OldPassword)
    NewPassword = ('New Password', 'newpassword', True, True, 'string', UserInfoType.NewPassword)

    Phone = ('Phone', 'phone', False, True, 'string', UserInfoType.Phone)
    CAPTCHA = ('CAPTCHA', 'CAPTCHA', False, True, 'string', UserInfoType.Pass)

    Id = ('Id', 'id', False, True, 'integer', UserInfoType.Pass)
    Content = ('Content', 'content', False, True, 'string', UserInfoType.Pass)

    ShowInvalid = ('ShowInvalidParam', 'show_invalid', False, True, 'boolean', UserInfoType.Pass)
    ManagerFirst = ('ManagerFirstParam', 'manager_first', False, True, 'boolean', UserInfoType.Pass)
    Page = ('Page', 'page', False, False, 'integer', UserInfoType.Pass)

    RealnameForModify = ('Name', 'realname', False, False, 'string', UserInfoType.RealName)
    MottoForModify = ('Motto', 'motto', False, False, 'string', UserInfoType.Pass)
    PermissionPublicForModify = (
        'Public Permission', 'permission_public', False, False, 'integer', UserInfoType.Pass
        )
    PermissionPrivateForModify = (
        'Private Permission', 'permission_private', False, False, 'integer', UserInfoType.Pass
        )

    ProgramName = ('Program Name', 'code_name', False, True, 'string', UserInfoType.Pass)
    ProgramCode = ('Program Code', 'code_content', False, True, 'string', UserInfoType.Pass)
    ProgramDoc = ('Program Document', 'code_readme', False, False, 'string', UserInfoType.Pass)

    ProgramId = ('Program ID', 'code_id', False, True, 'integer', UserInfoType.Pass)
    ProgramJudge = ('Program Judge', 'judge', False, True, 'integer', UserInfoType.Pass)

    Listype = ('List Type', 'sort_type', False, False, 'integer', UserInfoType.Pass)

    Description = ('Description', 'description', False, False, 'string', UserInfoType.Pass)

    Mine = ('List Mine', 'mine', False, True, 'boolean', UserInfoType.Pass)
    School = ('School', 'school', False, False, 'integer', UserInfoType.Pass)
    StatusUp = ('Status Upper Limit', 'status_up', False, False, 'integer', UserInfoType.Pass)
    StatusDown = ("Status Lower Limit", 'status_low', False, False, 'integer', UserInfoType.Pass)
    Theme = ('Theme', 'theme', False, False, 'integer', UserInfoType.Pass)

    Approve = ('Approve', 'approve', False, True, 'boolean', UserInfoType.Pass)
    SourceStatus = ('Source Status', 'source', False, True, 'integer', UserInfoType.Pass)
    TargetStatus = ('Target Status', 'target', False, True, 'integer', UserInfoType.Pass)

    ApplyListType = ('Apply List Type', 'type', False, False, 'integer', UserInfoType.Pass)
    ApplyId = ('Apply Id', 'apply_id', False, True, 'integer', UserInfoType.Pass)
    ApplyReason = ('Apply Message', 'apply_reason', False, True, 'string', UserInfoType.Pass)
    ApplySchoolId = (
        'Apply School Id', 'apply_school_id', False, True, 'integer', UserInfoType.Pass
        )

    SchoolName = ('School Name', 'school_name', False, True, 'string', UserInfoType.Pass)
    SchoolIdWithDefault = ('School Id', 'school_id', False, False, 'integer', UserInfoType.Pass)
    SchoolId = ('School Id', 'school_id', False, True, 'integer', UserInfoType.Pass)
    SchoolDescription = (
        'School Description', 'school_description', False, True, 'string', UserInfoType.Pass
        )

    ThemeId = ('Theme Id', 'theme_id', False, True, 'integer', UserInfoType.Pass)
    ThemeIdWithDefault = ('Theme Id', 'theme_id', False, False, 'integer', UserInfoType.Pass)
    ThemeName = ('Theme name', 'theme_name', False, True, 'string', UserInfoType.Pass)
    ThemeNameWithDefault = ('Theme name', 'theme_name', False, False, 'string', UserInfoType.Pass)
    ThemeDescription = (
        'Theme Description', 'theme_description', False, True, 'string', UserInfoType.Pass
    )
    ThemeDescriptionWithDefault = (
        'Theme Description', 'theme_description', False, False, 'string', UserInfoType.Pass
        )
    ThemeDeadline = (
        'Theme Deadline', 'theme_deadline', False, True, 'string', UserInfoType.Pass
    )
    ThemeDeadlineWithDefault = (
        'Theme Deadline', 'theme_deadline', False, False, 'string', UserInfoType.Pass
    )

    SearchText = ('Search Text', 'search_text', False, False, 'string', UserInfoType.Pass)
    TypeWithDefault = ('Type', 'type', False, False, 'integer', UserInfoType.Pass)

    CategoryId = ('Category ID', 'category_id', False, True, 'integer', UserInfoType.Pass)
    Filename = ('Filename', 'filename', False, True, 'string', UserInfoType.Pass)
    VideoTitle = ('Video Title', 'video_title', False, True, 'string', UserInfoType.Pass)
    FileKey = ('File Key', 'key', False, True, 'string', UserInfoType.Pass)
