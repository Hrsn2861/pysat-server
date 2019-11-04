"""pysat URL Configuration for School.Create
"""
from django.urls import path

from utils.views import view_maker
from utils.params import ParamType
from utils.permission import ActionType

from school.views import theme

urlpatterns = [
    path('create', view_maker(theme.create_theme, 'POST', [
        ParamType.SchoolIdWithDefault,
        ParamType.ThemeName,
        ParamType.ThemeDescription,
        ParamType.ThemeDeadline
    ], action=ActionType.ThemeCreate)),
    path('list', view_maker(theme.get_list, 'GET', [
        ParamType.SchoolId,
        ParamType.Page
    ], action=ActionType.UserGet))
]
