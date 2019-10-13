"""check params for request
"""

from enum import Enum
import server.utils.response as Response

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
        name, need, param_type = key.value
        if param_type not in ['string', 'integer', 'boolean']:
            return Response.failed_response("InvalidParams")

        if need is True and value is None:
            return Response.error_response("Invalid" + name)
        if param_type == 'boolean' and check_str_as_bool(value) is False:
            return Response.error_response("Invalid" + name)
        if param_type == 'integer' and check_str_as_int(value) is False:
            return Response.error_response("Invalid" + name)
    return None

class ParamType(Enum):
    """param types for function `check_params`
    """
    Token = ("Token", True, "string")
    Username = ("Username", True, "string")
    Password = ("Password", True, "string")
    Phone = ("Phone", True, "integer")
    CAPTCHA = ("CAPTCHA", True, "string")

    UsernameForInfo = ("Username", False, "string")
    
    ShowInvalidForUserList = ("show_invalid", True, "boolean")
    ManagerFirstForUserList = ("manager_first", True, "boolean")
    PageForUserList = ("page", True, "integer")