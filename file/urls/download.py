"""pysat URL Configuration for File Download
"""
from django.urls import path

from utils.views import view_maker
from utils.params import ParamType
import file.views.download as views

urlpatterns = [
    path('video', view_maker(views.video, 'GET', [
        ParamType.VideoID
    ]))
]
