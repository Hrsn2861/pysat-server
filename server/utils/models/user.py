"""
"""

import re
from django.contrib.auth.hashers import make_password, check_password

import server.utils.response as Response

from server.models import User
from server.utils.models.entrylog import get_entrylog


def query_to_user(user):
    """get user from item of queryset
    """
    if user is not None:
        return {
            'id' : user.id,
            'username' : user.username,
            'password' : user.password,
            'phone' : user.phone,
            'email' : user.email,
            'email_verify' : user.email_verify,
            'realname' : user.realname,
            'school' : user.school,
            'motto' : user.motto,
            'permission' : user.permission,
        }
    return None


def queryset_to_user(users):
    """get user from queryset
    """
    if users.exists():
        user = users.last()
        return query_to_user(user)
    return None


def user_filter(user):
    """delete some item of user for passing to frontend
    """
    if user is None:
        return None
    del user['password']
    del user['email_verify']
    return user


def get_user(user_id):
    """get user by `user_id`
    """
    if not isinstance(user_id, int):
        return None
    users = User.objects.filter(id=user_id)
    return queryset_to_user(users)


def get_user_by_username(username):
    """get user by `username`
    """
    if not isinstance(username, str):
        return None
    users = User.objects.filter(username=username)
    return queryset_to_user(users)


def get_user_by_phone(phone):
    """get user by `phone`
    """
    if not isinstance(phone, str):
        return None
    users = User.objects.filter(phone=phone)
    return queryset_to_user(users)


def get_user_by_session(session_id):
    """get user by session id
    """
    entrylog = get_entrylog(session_id)
    if entrylog is None:
        return None
    user_id = entrylog['user_id']
    return get_user(user_id)


def signup(userinfo):
    """signup

    requirement:
    - username
    - password
    - phone
    - permission
    """
    if not isinstance(userinfo.get('username'), str):
        return None
    if not isinstance(userinfo.get('password'), str):
        return None
    if not isinstance(userinfo.get('phone'), str):
        return None
    if not isinstance(userinfo.get('permission'), int):
        return None
    user = User(
        username=userinfo['username'],
        password=make_password(userinfo['password']),
        phone=userinfo['phone'],
        permission=userinfo['permission']
    )
    user.save()
    return user.id


def signin_check_password(user, password):
    """check the password for sign in (for user)
    """
    if user is None:
        return False
    return check_password(password, user['password'])


def signin_check(user_id, password):
    """check the password for sign in (for user_id)
    """
    user = get_user(user_id)
    return signin_check_password(user, password)


def modify_user(user_id, info):
    """modify user's info
    """
    if not isinstance(user_id, int):
        return False
    users = User.objects.filter(id=user_id)
    if users.exists():
        user = users.last()
    else:
        return False

    realname = info.get('realname')
    school = info.get('school')
    motto = info.get('motto')
    permission = info.get('permission')
    password = info.get('password')

    if isinstance(realname, str):
        user.realname = realname
    if isinstance(school, str):
        user.school = school
    if isinstance(motto, str):
        user.motto = motto
    if isinstance(permission, int):
        user.permission = permission
    if UserInfoChecker.check_password(password):
        user.password = make_password(password)

    user.save()
    return True


def user_count(show_invalid=False):
    """get the number of user
    """
    if show_invalid is True:
        qs = User.objects.all()
    else:
        qs = User.objects.filter(permission__gt=0)
    return qs.count()


def user_list(page, show_invalid=False, manager_first=False):
    """get user list
    """
    if not isinstance(page, int):
        return []

    if show_invalid is True:
        qs = User.objects.all()
    else:
        qs = User.objects.filter(permission__gt=0)
    if manager_first is True:
        qs = qs.order_by('-permission', 'id')
    else:
        qs = qs.order_by('id')

    users = qs[(page - 1) * 20 : page * 20]
    ret = []
    for user in users:
        user = query_to_user(user)
        ret.append(user_filter(user))
    return ret


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
        for (func, name), value in params.items():
            if func(value) is not True:
                return Response.error_response("Illegal" + name)
        return None
