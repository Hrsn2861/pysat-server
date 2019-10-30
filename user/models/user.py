"""Models about user
"""
from django.db import models
from django.contrib.auth.hashers import make_password, check_password

from utils.checker import UserInfoChecker
from user.models.entrylog import EntryLogHelper

class User(models.Model):
    """User
    """
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=128)
    phone = models.CharField(max_length=11)

    email = models.CharField(max_length=64, default='')
    email_verify = models.CharField(max_length=64, default='')

    realname = models.CharField(max_length=32, default='')
    motto = models.CharField(max_length=256, default='')

    permission = models.IntegerField(default=1)

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        get_latest_by = 'id'

class UserHelper:
    """User Helper for pysat-server

    It contains some functions about user operation.
    """

    @staticmethod
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
                'motto' : user.motto,
                'permission' : user.permission,
            }
        return None

    @staticmethod
    def queryset_to_user(users):
        """get user from queryset
        """
        if users.exists():
            user = users.last()
            return UserHelper.query_to_user(user)
        return None

    @staticmethod
    def user_filter(user):
        """delete some item of user for passing to frontend
        """
        if user is None:
            return None
        del user['password']
        del user['email_verify']
        return user

    @staticmethod
    def get_user(user_id):
        """get user by `user_id`
        """
        if not isinstance(user_id, int):
            return None
        users = User.objects.filter(id=user_id)
        return UserHelper.queryset_to_user(users)

    @staticmethod
    def get_name_by_id(user_id):
        """get username by userid
        """
        user = UserHelper.get_user(user_id)
        if user is None:
            return '-'
        return user['username']

    @staticmethod
    def get_user_by_username(username):
        """get user by `username`
        """
        if not isinstance(username, str):
            return None
        users = User.objects.filter(username=username)
        return UserHelper.queryset_to_user(users)

    @staticmethod
    def get_user_by_phone(phone):
        """get user by `phone`
        """
        if not isinstance(phone, str):
            return None
        users = User.objects.filter(phone=phone)
        return UserHelper.queryset_to_user(users)

    @staticmethod
    def get_user_by_session(session_id):
        """get user by session id
        """
        entrylog = EntryLogHelper.get_entrylog(session_id)
        if entrylog is None:
            return None
        user_id = entrylog['user_id']
        return UserHelper.get_user(user_id)

    @staticmethod
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

    @staticmethod
    def signin_check_password(user, password):
        """check the password for sign in (for user)
        """
        if user is None:
            return False
        return check_password(password, user['password'])

    @staticmethod
    def signin_check(user_id, password):
        """check the password for sign in (for user_id)
        """
        user = UserHelper.get_user(user_id)
        return UserHelper.signin_check_password(user, password)

    @staticmethod
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
        # school = info.get('school')
        # schoolid = info.get('schoolid')
        motto = info.get('motto')
        # permission = info.get('permission')
        password = info.get('password')
        phone = info.get('phone')

        if isinstance(realname, str):
            user.realname = realname
        # if isinstance(school, str):
        #     user.school = school
        if isinstance(motto, str):
            user.motto = motto
        # if isinstance(permission, int):
        #    user.permission = permission
        if UserInfoChecker.check_password(password):
            user.password = make_password(password)
        if UserInfoChecker.check_phone(phone):
            user.phone = phone
        # if isinstance(schoolid, int):
        #     user.schoolid = schoolid

        user.save()
        return True

    @staticmethod
    def user_count(show_invalid=False):
        """get the number of user
        """
        if show_invalid is True:
            qs = User.objects.all()
        else:
            qs = User.objects.filter(permission__gt=0)
        return qs.count()

    @staticmethod
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
            user = UserHelper.query_to_user(user)
            ret.append(UserHelper.user_filter(user))
        return ret
