"""pysat URL Configuration for message.message
"""
from django.urls import path

from utils.views import view_maker
from utils.params import ParamType
from utils.permission import ActionType

from message.views import message

urlpatterns = [
    path('list', view_maker(message.get_list, 'POST', [
        ParamType.Username,
        ParamType.Page
    ], action=ActionType.NormalUser)),
    path('send', view_maker(message.send, 'POST', [
        ParamType.Username,
        ParamType.Content
    ], action=ActionType.NormalUser)),
    path('undo', view_maker(message.undo, 'POST', [
        ParamType.Id
    ], action=ActionType.NormalUser))
]
