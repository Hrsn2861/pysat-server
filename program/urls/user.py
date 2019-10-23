"""pysat URL Configuration for Program.User
"""
from django.urls import path

from utils.views import view_maker
from utils.params import ParamType
from utils.permission import ActionType
from program.views import user

urlpatterns = [
    path('submit', view_maker(user.submit, 'POST', [
        ParamType.ProgramName,
        ParamType.ProgramCode,
        ParamType.ProgramDoc
    ], action=ActionType.SubmitProgram)),
]
