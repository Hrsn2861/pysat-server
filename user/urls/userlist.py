"""pysat URL Configuration for User.List
"""
from django.urls import path

from utils.views import view_maker
from utils.params import ParamType
from utils.permission import ActionType

from user.views import userlist

urlpatterns = [
    path('get', view_maker(userlist.getlist, 'GET', [
        ParamType.ShowInvalid,
        ParamType.ManagerFirst,
        ParamType.SchoolId,
        ParamType.Page
    ], action=ActionType.GetAllUserList))
]
