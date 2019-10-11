"""send a message to phone
"""

from server.utils.models.user import UserInfoChecker

def send(phone, msg):
    """send msg
    """
    if not UserInfoChecker.check_phone(phone):
        return False
    if not isinstance(msg, str):
        return False
    return True

def send_verify_code(phone, code):
    """send verify code
    """
    if not isinstance(code, str):
        return False
    return send(phone, "Verify Code is " + code)
