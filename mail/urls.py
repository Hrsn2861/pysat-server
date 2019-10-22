"""pysat URL Configuration for Mail
"""
from django.urls import path

from utils.views import view_maker
from utils.params import ParamType
from mail.views import mail_show

urlpatterns = [
    path('show', view_maker(mail_show, 'GET', [
        ParamType.MailId
    ]))
]
