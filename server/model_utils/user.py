"""
"""

from server.models import User
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
            'valid' : users[0].valid
        }
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


def signup(username, password, email, telphone, realname, school, permission = 1):
    user = User(username=username, password=make_password(password), email=email, telphone=telphone, realname=realname, school=school, permission=permission)
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

    user.save()


class UserInfoChecker:
    """UserInfo Checker
    """

    @staticmethod
    def check_password(password):
        return True

    @staticmethod
    def check_email(email):
        return True

    @staticmethod
    def check_realname(realname):
        return True

    @staticmethod
    def check_school(school):
        return True

    @staticmethod
    def check_telphone(telphone):
        return True