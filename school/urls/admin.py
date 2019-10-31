"""pysat URL Configuration for School.admin
"""
from django.urls import path

from utils.views import view_maker
from utils.params import ParamType
from utils.permission import ActionType

from school.views import admin

urlpatterns = [
    path('approve', view_maker(admin.approve, 'POST', [
        ParamType.Username,
        ParamType.Approve
    ], action=ActionType.Approve))
]
