"""Models about verify
"""
from django.db import models

from user.models.user import User, UserHelper

class Permission(models.Model):
    """Permission
    """
    user_id = models.IntegerField()
    school_id = models.IntegerField()
    permission = models.IntegerField()

    class Meta:
        verbose_name = 'permission'
        verbose_name_plural = 'permissions'
        get_latest_by = 'id'

class PermissionHelper:
    """User Helper for pysat-server

    It contains some functions about user operation.
    """

    @staticmethod
    def set_permission(user_id, school_id, permission):
        """set permission
        """
        perms = Permission.objects.filter(user_id=user_id, school_id=school_id)
        if perms.exists():
            perm = perms.last()
            perm.permission = permission
            perm.save()
        else:
            perm = Permission(user_id=user_id, school_id=school_id, permission=permission)
            perm.save()

    @staticmethod
    def get_permission(user_id, school_id):
        """get permission
        """
        user = UserHelper.get_user(user_id)
        if user is None:
            return 0
        if user['permission'] > 3:
            return user['permission']
        perms = Permission.objects.filter(user_id=user_id, school_id=school_id)
        if perms.exists():
            perm = perms.last()
            return perm.permission
        if school_id == 0:
            return user['permission']
        return -1

    @staticmethod
    def get_user_school(user_id):
        """get user's school
        """
        perms = Permission.objects.filter(user_id=user_id, school_id__gt=0)
        if perms.exists():
            return perms.last().school_id
        return 0

    @staticmethod
    def user_quit_school(user_id):
        """quit school
        """
        perms = Permission.objects.filter(user_id=user_id, school_id__gt=0)
        for perm in perms:
            perm.delete()

    @staticmethod
    def user_join_school(user_id, school_id):
        """ join school
        """
        PermissionHelper.user_quit_school(user_id)
        PermissionHelper.set_permission(user_id, school_id, 1)

    @staticmethod
    def set_user_permission(user_id, permission):
        """set user permission
        """
        users = User.objects.filter(id=user_id)
        if users.exists():
            user = users.last()
            user.permission = permission
            user.save()
            return True
        return False

    @staticmethod
    def get_school_population(school_id):
        """ get a school's population
        """
        perms = Permission.objects.filter(school_id=school_id)
        return perms.count()

    @staticmethod
    def get_school_headmaster(school_id):
        """ get a school's headmaster(permission = 4)
        """
        perms = Permission.objects.filter(school_id=school_id, permission=4)
        if perms.exist():
            return perms.last().user_id
        return 0
