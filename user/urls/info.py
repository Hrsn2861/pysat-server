"""pysat URL Configuration for User.Info
"""
from django.urls import path

from utils.views import view_maker
from utils.params import ParamType
from utils.permission import ActionType

from user.views import info

urlpatterns = [
    path('get', view_maker(info.get_info, 'GET', [
        ParamType.UsernameWithDefault
    ], action=ActionType.GetUserInfo)),
    path('modify', view_maker(info.modify_info, 'POST', [
        ParamType.UsernameWithDefault,
        ParamType.RealnameForModify,
        ParamType.SchoolForModify,
        ParamType.MottoForModify,
        ParamType.PermissionForModify
    ], [
        ParamType.RealnameForModify,
        ParamType.SchoolForModify,
        ParamType.MottoForModify,
        ParamType.PermissionForModify
    ])),
    path('setphone', view_maker(info.set_phone, 'POST', [
        ParamType.Phone,
        ParamType.CAPTCHA
    ], [
        ParamType.Phone
    ], action=ActionType.ModifyMyInfo))
]
