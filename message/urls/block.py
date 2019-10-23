"""pysat URL Configuration for message.chat
"""
from django.urls import path

from utils.views import view_maker
from utils.params import ParamType
from utils.permission import ActionType

from message.views import block

urlpatterns = [
    path('list', view_maker(block.get_list, 'POST', action=ActionType.NormalUser)),
    path('set', view_maker(block.set_block, 'POST', [
        ParamType.Username
    ], action=ActionType.NormalUser)),
    path('unset', view_maker(block.unset_block, 'POST', [
        ParamType.Username
    ], action=ActionType.NormalUser))
]
