"""pysat URL Configuration for File Upload
"""
from django.urls import path

from utils.views import view_maker
import file.views.upload as views

urlpatterns = [
    path('test', view_maker(views.test, 'POST'))
]
