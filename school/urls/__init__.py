"""pysat URL Configuration for School
"""

from django.conf.urls import url, include

from . import school
from . import user
from . import admin

urlpatterns = [
    url(r'^school/', include(school)),
    url(r'^user/', include(user)),
    url(r'^admin/', include(admin))
]
