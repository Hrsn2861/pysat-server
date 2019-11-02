"""pysat URL Configuration for Program.Admin
"""
from django.urls import path

from utils.views import view_maker
from utils.params import ParamType
from utils.permission import ActionType
from program.views import proglist

urlpatterns = [
    path('get', view_maker(proglist.get_program_list, 'GET', [
        ParamType.Mine,
        ParamType.SchoolIdWithDefault,
        ParamType.StatusUp,
        ParamType.StatusDown,
        ParamType.Listype,
        ParamType.ThemeIdWithDefault,
        ParamType.Page
    ], action=ActionType.UserGet))
]
