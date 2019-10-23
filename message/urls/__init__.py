"""pysat URL Configuration for Message
"""
from django.conf.urls import url, include

from message.urls import message

urlpatterns = [
    url(r'^message/', include(message))
]
