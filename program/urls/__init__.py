"""pysat URL Configuration for Program
"""
from django.conf.urls import url, include

from . import user
from . import admin
from . import proglist

urlpatterns = [
    url(r'^user/', include(user)),
    url(r'^admin/', include(admin)),
    url(r'^list/', include(proglist))
]
