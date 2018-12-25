#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : auth.py
# @Author: Lcy
# @Date  : 2018/11/30
# @Desc  : 用户认证

from rest_framework.authentication import BaseAuthentication
from ..models import UserToken
from rest_framework import exceptions
import datetime
class Authentication(BaseAuthentication):

    def authenticate(self, request):

        # 从header中获取token
        token = request.META.get('HTTP_X_CSRFTOKEN')
        obj = UserToken.objects.filter(token=token).first()

        # 判断token有效期
        if not obj:
            raise exceptions.AuthenticationFailed('用户认证失败')
        else:
            create_time = obj.createtime
            now_time = datetime.datetime.now()
            # token有效期是1天( 24*60*60 )
            if (now_time - create_time).seconds > 24*60*60:
                raise exceptions.AuthenticationFailed('用户认证失败')
            else:
                return (obj.user, obj)



    def authenticate_header(self, request):
        pass

