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
import server.posts.user_sign as user_sign
import server.posts.user_info as user_info

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', server.views.test_database),
    
    path('check_login/', user_sign.check_login),
    path('signin/', user_sign.signin),
    path('signup/', user_sign.signup),
    path('userinfo/',user_info.user_info)
]
