"""pysat URL Configuration for Session
"""
from django.urls import path

from utils.views import view_maker
from utils.params import ParamType
from session.views import start_session, check_session

urlpatterns = [
    path('start', view_maker(start_session, 'POST')),
    path('check', view_maker(check_session, 'GET', [ParamType.Token]))
]
