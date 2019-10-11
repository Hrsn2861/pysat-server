"""pysat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

import server.views
import server.requests.session as session
import server.requests.user_sign as user_sign
import server.requests.user_info as user_info

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', server.views.test),

    path('session/start', session.start_session),
    path('session/check', session.check_session),

    path('user/sign/login', user_sign.signin),
    path('user/sign/register', user_sign.signup),
    path('user/sign/logout', user_sign.signout),

    path('user/info/get', user_info.get_info)

]
