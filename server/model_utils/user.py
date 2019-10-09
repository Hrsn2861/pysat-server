"""
"""

import re

from server.models import User
from server.model_utils.entrylog import randkey
from django.contrib.auth.hashers import make_password, check_password


def getFirstUserInList(users):
    if len(users) > 0:
        ret = {
            'id' : users[0].id,
            'username' : users[0].username,
            'password' : users[0].password,
            'email' : users[0].email,
            'telphone' : users[0].telphone,
            'realname' : users[0].realname,
            'school' : users[0].school,
            'motto' : users[0].motto,
            'permission' : users[0].permission,
            'valid' : users[0].valid,
            'verify' : users[0].verify
        }
        ret['need_verify'] = (True if users[0].verify is not "" else False)
        return ret
    else:
        return None


def getUser(userid):
    users = User.objects.filter(id=int(userid))
    return getFirstUserInList(users)


def getUserByName(username):
    users = User.objects.filter(username=str(username))
    return getFirstUserInList(users)


def getUserByTelphone(telphone):
    users = User.objects.filter(telphone=str(telphone))
    return getFirstUserInList(users)


def signup(userinfo):
    user = User(
        username=userinfo['username'],
        password=make_password(userinfo['password']),
        email=userinfo['email'],
        telphone=userinfo['telphone'],
        realname=userinfo['realname'],
        school=userinfo['school'],
        permission=userinfo['permission'],
        verify=randkey(length=6)
    )
    user.save()
    return user.id


def signin(userid, password):
    user = getUser(userid)
    if user is None:
        return False
    if user['valid'] is not True:
        return False
    return check_password(password, user['password'])


def modifyUser(userid, info):
    users = User.objects.filter(id=int(userid))
    if len(users) != 1:
        return False
    user = users[0]

    realname = info.get('realname')
    school = info.get('school')
    motto = info.get('motto')
    permission = info.get('permission')
    password = info.get('password')
    verify = info.get('verify')

    if realname is not None:
        user.realname = realname
    if school is not None:
        user.school = school
    if motto is not None:
        user.motto = motto
    if permission is not None:
        user.permission = permission
    if password is not None:
        user.password = make_password(password)
    if verify is not None:
        user.verify = verify

    user.save()


def user_verify(userid, verify_key):
    user = getUser(userid)
    if user is not None and user['need_verify'] is True:
        if verify_key == user['verify']:
            modifyUser(userid, {'verify' : ''})
            return True
    return False


def user_count(manager=False, show_invalid=False):
    condtions = {}
    if manager:
        condtions['permission__gt'] = 1
    else:
        condtions['permission'] = 1
    if not show_invalid:
        condtions['valid'] = True
    return User.objects.filter(**condtions).count()


def user_list(page, manager=False, show_invalid=False):
    condtions = {}
    if manager:
        condtions['permission__gt'] = 1
    else:
        condtions['permission'] = 1
    if not show_invalid:
        condtions['valid'] = True
    qs = User.objects.filter(**condtions).order_by('id')
    users = qs[(page - 1) * 20 : page * 20]
    ret = []
    for user in users:
        user = getFirstUserInList([user])
        del user['password']
        del user['verify']
        ret.append(user)
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
        if username is None:
            return False
        username = str(username)
        if len(username) < 4 or len(username) > 16:
            return False
        if username.isdigit():
            return False
        if not username.isalnum():
            return False
        return True

    @staticmethod
    def check_password(password):
        """检验密码合理性

        必须包含大写字母、小写字母、数字
        特殊字符只支持 ~!@&%#_
        长度在 6-20 位之间
        """
        if password is None:
            return False
        password = str(password)
        if re.findall(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])[a-zA-Z0-9~!@&%#_]{6,20}$', password):
            return True
        return False

    @staticmethod
    def check_email(email):
        """检验邮箱合理性
        """
        if email is None:
            return False
        email = str(email)
        if re.findall(r'^\w+@(\w+.)+(com|cn|net)$', email):
            return True
        return False

    @staticmethod
    def check_realname(realname):
        """检验姓名合理性
        """
        if realname is None:
            return False
        return True

    @staticmethod
    def check_school(school):
        """检验学校合理性
        """
        if school is None:
            return False
        return True

    @staticmethod
    def check_telphone(telphone):
        """检验电话合理性

        十一位的纯数字
        """
        if telphone is None:
            return False
        telphone = str(telphone)
        if len(telphone) != 11:
            return False
        if not telphone.isdigit():
            return False
        return True