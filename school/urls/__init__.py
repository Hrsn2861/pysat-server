"""pysat URL Configuration for School
"""

from django.conf.urls import url, include

from . import school
from . import user

urlpatterns = [
    url(r'^school/', include(school)),
    url(r'^user/', include(user))
]
