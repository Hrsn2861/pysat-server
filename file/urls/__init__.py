"""pysat URL Configuration for File Upload
"""
from django.conf.urls import url, include

from . import download
from . import upload

urlpatterns = [
    url(r'^download/', include(download)),
    url(r'^upload/', include(upload))
]
