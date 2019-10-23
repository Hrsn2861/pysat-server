"""pysat URL Configuration for Program.Admin
"""
from django.urls import path

from utils.views import view_maker
from utils.params import ParamType
from utils.permission import ActionType
from program.views import admin

urlpatterns = [
    path('upload', view_maker(admin.upload, 'POST', [
        ParamType.ProgramId
    ], action=ActionType.AdminUploadProgram)),
    path('judge', view_maker(admin.judge, 'POST', [
        ParamType.ProgramId,
        ParamType.ProgramJudge
    ], action=ActionType.AdminJudge))
]
