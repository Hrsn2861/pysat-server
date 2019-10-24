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
    if value.isdigit():
        return True
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
    SchoolForModify = ('School', 'school', False, False, 'string', UserInfoType.School)
    MottoForModify = ('Motto', 'motto', False, False, 'string', UserInfoType.Pass)
    PermissionForModify = ('Permission', 'permission', False, False, 'integer', UserInfoType.Pass)

    ProgramName = ('Program Name', 'codename', False, True, 'string', UserInfoType.Pass)
    ProgramCode = ('Program Code', 'code', False, True, 'string', UserInfoType.Pass)
    ProgramDoc = ('Program Document', 'readme', False, False, 'string', UserInfoType.Pass)

    ProgramId = ('Program ID', 'codeid', False, True, 'integer', UserInfoType.Pass)
    ProgramJudge = ('Program Judge', 'judge', False, True, 'integer', UserInfoType.Pass)

    Listype = ('List Type', 'type', False, True, 'integer', UserInfoType.Pass)
