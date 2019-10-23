"""pysat URL Configuration for Program.Admin
"""
from django.urls import path

from utils.views import view_maker
from utils.params import ParamType
from utils.permission import ActionType
from program.views import proglist

urlpatterns = [
    path('onstar', view_maker(proglist.onstar_list, 'GET', [
        ParamType.Listype,
        ParamType.Page
    ], action=ActionType.UserGet)),

    path('mine', view_maker(proglist.mylist, 'GET', [
        ParamType.Page
    ], action=ActionType.UserGet)),

    path('inqueue', view_maker(proglist.inqueue_list, 'GET', [
        ParamType.Page
    ], action=ActionType.UserGet)),

    path('judge', view_maker(proglist.judge_list, 'GET', [
        ParamType.Page
    ], action=ActionType.UserGet))
]
