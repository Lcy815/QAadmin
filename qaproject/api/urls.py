#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : urls.py
# @Author: Lcy
# @Date  : 2018/11/28
# @Desc  : urls

from django.urls import path
from .views.UserLoginViews import Login, GetUserInfo, LoginOut

urlpatterns = [
    path('login/login', Login.as_view()),
    path('user/info', GetUserInfo.as_view()),
    path('login/logout', LoginOut.as_view())
]