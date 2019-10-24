"""pysat URL Configuration for message.chat
"""
from django.urls import path

from utils.views import view_maker
from utils.permission import ActionType

from message.views import chat

urlpatterns = [
    path('list', view_maker(chat.get_list, 'POST', action=ActionType.NormalUser))
]
