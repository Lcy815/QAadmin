#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : urls.py
# @Author: Lcy
# @Date  : 2018/11/28
# @Desc  : urls

from django.urls import path
from .views.UserLoginViews import Login, GetUserInfo, LoginOut
from .views.UserManage import GetAllUser, UserDetail
from .views.ProjectManage import Project, Module
urlpatterns = [
    # 用户管理相关
    path('login/login', Login.as_view()),
    path('user/info', GetUserInfo.as_view()),
    path('login/logout', LoginOut.as_view()),
    path('user/users', GetAllUser.as_view()),
    path('user/detail', UserDetail.as_view()),
    path('user/search', GetAllUser.as_view()),
    # 项目管理相关
    path('project/project',Project.as_view()),
    path('project/modules', Module.as_view())

]