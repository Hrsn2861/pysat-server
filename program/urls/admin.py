"""pysat URL Configuration for Program.Admin
"""
from django.urls import path

from utils.views import view_maker
from utils.params import ParamType
from utils.permission import ActionType
from program.views import admin

urlpatterns = [
    path('download', view_maker(admin.download, 'GET', [
        ParamType.ProgramId
    ], action=ActionType.AdminUploadProgram)),

    path('status', view_maker(admin.change_status, 'POST', [
        ParamType.ProgramId,
        ParamType.SourceStatus,
        ParamType.TargetStatus
    ], action=ActionType.AdminChangeStatus))
]
