"""Some checkers
"""
from enum import Enum

import re
import utils.response as Response

class UserInfoChecker:
    """UserInfo Checker
    """

    @staticmethod
    def check_username(username):
        """检验用户名合理性

        必须包含字母
        只能包含字母与数字
        长度在 4-16 位之间
        """
        if not isinstance(username, str):
            return False
        if re.findall(r'^(?=.*[a-zA-Z])[a-zA-Z0-9]{4,16}$', username):
            return True
        return True

    @staticmethod
    def check_password(password):
        """检验密码合理性

        必须包含大写字母、小写字母、数字
        特殊字符只支持 ~!@&%#_
        长度在 6-20 位之间
        """
        if not isinstance(password, str):
            return False
        if re.findall(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])[a-zA-Z0-9~!@&%#_]{6,20}$', password):
            return True
        return False

    @staticmethod
    def check_email(email):
        """检验邮箱合理性
        """
        if not isinstance(email, str):
            return False
        email = str(email)
        if re.findall(r'^\w+@(\w+.)+(com|cn|net)$', email):
            return True
        return False

    @staticmethod
    def check_realname(realname):
        """检验姓名合理性
        """
        if not isinstance(realname, str):
            return False
        return True

    @staticmethod
    def check_school(school):
        """检验学校合理性
        """
        if not isinstance(school, str):
            return False
        return True

    @staticmethod
    def check_phone(phone):
        """检验电话合理性

        十一位的纯数字
        """
        if not isinstance(phone, str):
            return False
        if re.findall(r'^1[0-9]{10}$', phone):
            return True
        return False

    @staticmethod
    def check(params):
        """检验 param 中的参数
        """
        for key, value in params.items():
            name, func = key.value
            if value is None:
                continue
            if func(value) is not True:
                return Response.error_response("Illegal " + name)
        return None

class UserInfoType(Enum):
    """UserInfo for checker

    UserInfoType.Key = (name, function)
    """
    Pass = ('', lambda _: True)
    Username = ('Username', UserInfoChecker.check_username)
    Password = ('Password', UserInfoChecker.check_password)
    OldPassword = ('Old Password', UserInfoChecker.check_password)
    NewPassword = ('New Password', UserInfoChecker.check_password)
    Phone = ('Phone', UserInfoChecker.check_phone)
    Email = ('E-mail', UserInfoChecker.check_email)
    RealName = ('Name', UserInfoChecker.check_realname)
    School = ('School', UserInfoChecker.check_school)
