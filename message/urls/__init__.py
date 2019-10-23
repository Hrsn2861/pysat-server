"""pysat URL Configuration for Message
"""
from django.conf.urls import url, include

from message.urls import message
from message.urls import chat

urlpatterns = [
    url(r'^message/', include(message)),
    url(r'^chat/', include(chat))
]
