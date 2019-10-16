"""pysat URL Configuration for User
"""
from django.conf.urls import url, include

from . import sign
from . import info
from . import userlist

urlpatterns = [
    url(r'^sign/', include(sign)),
    url(r'^info/', include(info)),
    url(r'^list/', include(userlist))
]
