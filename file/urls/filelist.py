"""pysat URL Configuration for File List
"""
from django.urls import path

from utils.views import view_maker
from utils.params import ParamType
import file.views.filelist as views

urlpatterns = [
    path('info', view_maker(views.info, 'GET', [
        ParamType.SchoolId,
        ParamType.CategoryId,
        ParamType.Page
    ]))
]
