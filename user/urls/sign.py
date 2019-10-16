"""pysat URL Configuration for User.Sign
"""
from django.urls import path

from utils.views import view_maker
from utils.params import ParamType

from user.views import sign

urlpatterns = [
    path('login', view_maker(sign.signin, 'POST', [
        ParamType.Username,
        ParamType.Password
    ], [
        ParamType.Username,
        ParamType.Password
    ])),
    path('register', view_maker(sign.signup, 'POST', [
        ParamType.Username,
        ParamType.Password,
        ParamType.Phone,
        ParamType.CAPTCHA
    ], [
        ParamType.Username,
        ParamType.Password,
        ParamType.Phone
    ])),
    path('logout', view_maker(sign.signout, 'POST')),
    path('verify', view_maker(sign.verify_phone, 'POST', [
        ParamType.Phone
    ], [
        ParamType.Phone
    ])),
    path('modify', view_maker(sign.change_password, 'POST', [
        ParamType.OldPassword,
        ParamType.NewPassword
    ], [
        ParamType.OldPassword,
        ParamType.NewPassword
    ]))
]
