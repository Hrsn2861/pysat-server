"""permission manager
"""
from enum import Enum

class ActionType(Enum):
    """Action Type
    """
    GetUserInfo = 1
    ModifyMyInfo = 1
    ModifyUserInfo = 5

    GetUserList = 1
    GetAllUserList = 4

    SubmitProgram = 1

    AdminUploadProgram = 4
    AdminJudge = 4

    UserLike = 1
    UserDownload = 1
    UserGet = 1

    SetBan = 4

    UselessAction = 512
    BannedAction = 512

    BannedUser = 0
    NormalUser = 1
    Teacher = 2
    Master = 3
    Manager = 4
    SuperManager = 8

    CreateSchool = 8
    ApplyForSchool = 1

    Approve = 2

class PermissionManager:
    """Permission Manager
    """
    @staticmethod
    def check_permission(permission, action):
        """check if user with permission is allowed to do someaction
        """
        return permission >= action.value

    @staticmethod
    def check_user(user, action):
        """check if user is allowed to do someaction
        """
        if user is None:
            return False
        if 'permission' not in user:
            return False
        permission = user.get('permission')
        permission = int(permission)
        return PermissionManager.check_permission(permission, action)

    @staticmethod
    def get_identity(permission):
        """get the identity of user according to permission
        """
        if PermissionManager.check_permission(permission, ActionType.SuperManager):
            return ActionType.SuperManager
        if PermissionManager.check_permission(permission, ActionType.Manager):
            return ActionType.Manager
        if PermissionManager.check_permission(permission, ActionType.Teacher):
            return ActionType.Teacher
        if PermissionManager.check_permission(permission, ActionType.Master):
            return ActionType.Master
        if PermissionManager.check_permission(permission, ActionType.NormalUser):
            return ActionType.NormalUser
        return ActionType.BannedUser

    @staticmethod
    def promote_to_action(old_permission, new_permission):
        """get the action according to permission changes
        """
        if old_permission == new_permission:
            return ActionType.UselessAction
        old_identity = PermissionManager.get_identity(old_permission)
        new_identity = PermissionManager.get_identity(new_permission)
        if ActionType.SuperManager in [old_identity, new_identity]:
            return ActionType.BannedAction
        if ActionType.Manager in [old_identity, new_identity]:
            return ActionType.SuperManager
        return ActionType.SetBan

    @staticmethod
    def modify_to_action(session_user, target_user, info):
        """get the action according to modify behavior
        """
        if session_user.get('id') == target_user.get('id'):
            # modify self
            if info.get('permission') is not None:
                return ActionType.BannedAction
            return ActionType.ModifyMyInfo
        if 'permission' in info:
            if len(info) > 1:
                return ActionType.BannedAction
            return PermissionManager.promote_to_action(
                target_user.get('permission'), info.get('permission'))
        return ActionType.ModifyUserInfo
