"""Models about verify
"""
from django.db import models

from user.models import User, UserHelper

class Permission(models.Model):
    """VerifyCode
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
        return 0

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
