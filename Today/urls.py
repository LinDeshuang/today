"""Today URL Configuration

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
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token

import xadmin
from django.contrib import admin
from django.urls import path, include
from django.views.static import serve
from rest_framework.authtoken import views
from Today.settings import MEDIA_ROOT
from rest_framework import routers

from todo.views import TodoViewset
from user.views import SendEmailViewset, UserViewset

router = DefaultRouter()
# 验证码
router.register(r'code', SendEmailViewset, basename="code")
# 用户
router.register(r'user', UserViewset, base_name="user")
# 代办事项
router.register(r'todo', TodoViewset, base_name="todo")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('xadmin/', xadmin.site.urls),
    # drf自带的认证模式token
    path('api-token-auth/', views.obtain_auth_token),
    # jwt auth
    path('login/', obtain_jwt_token),
    path('', include(router.urls)),
    # drf文档功能引入
    path('docs/', include_docs_urls(title='Today')),
    path('media/<path:path>', serve, {"document_root": MEDIA_ROOT}),
]
