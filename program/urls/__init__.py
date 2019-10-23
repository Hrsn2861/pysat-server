"""pysat URL Configuration for Program
"""
from django.conf.urls import url, include

from . import user
from . import admin

urlpatterns = [
    url(r'^user/', include(user)),
    url(r'^admin/', include(admin))
]
