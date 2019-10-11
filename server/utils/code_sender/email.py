"""send an email
"""

from server.utils.models.user import UserInfoChecker

def send(email, msg):
    """send msg
    """
    if not UserInfoChecker.check_email(email):
        return False
    if not isinstance(msg, str):
        return False
    return True

def send_verify_code(email, code):
    """send verify code
    """
    if not isinstance(code, str):
        return False
    return send(email, "Verify Code is " + code)
