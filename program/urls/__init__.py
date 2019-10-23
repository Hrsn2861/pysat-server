"""pysat URL Configuration for Program
"""
from django.conf.urls import url, include

from . import user

urlpatterns = [
    url(r'^user/', include(user))
]
