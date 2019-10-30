"""pysat URL Configuration for School
"""

from django.conf.urls import url, include

from . import school

urlpatterns = [
    url(r'^school/', include(school))
]
