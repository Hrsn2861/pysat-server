"""pysat URL Configuration for Message
"""
from django.conf.urls import url, include

from message.urls import message
from message.urls import chat
from message.urls import block

urlpatterns = [
    url(r'^message/', include(message)),
    url(r'^chat/', include(chat)),
    url(r'^block/', include(block))
]
