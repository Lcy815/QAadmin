#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : UserManage.py
# @Author: Lcy
# @Date  : 2018/12/4
# @Desc  : 用户管理相关
from rest_framework.views import APIView, Request
from django.http import HttpResponse, JsonResponse
from api.models import userModels
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from ..utils.parser import Parser
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
import django_filters

class UserSerializer(serializers.ModelSerializer):

    # id = serializers.IntegerField()
    username = serializers.CharField(validators=[UniqueValidator(queryset=userModels.UserInfo.objects.all(), message='用户名重复')])
    # roles = serializers.CharField(source='get_roles_display')
    # avatar = serializers.CharField()
    class Meta:
        model = userModels.UserInfo
        fields = ('username', 'password', 'roles', 'introduction', 'avatar', 'id', 'email')

    # def validate(self, attrs):
    #     print(attrs)
    #     if userModels.UserInfo.objects.filter(username=attrs['username']).exists():
    #         raise serializers.ValidationError('username has exists')

class UserFilter(django_filters.FilterSet):
    class Meta:
        model = userModels.UserInfo
        fields = ['username']

class GetAllUser(APIView):

    authentication_classes = []
    def get(self, request):
        ret = {
            'code': 1000,
            'msg': None,
            'total': 0,
            'data': [],
            'page_size': 3
        }
        param = Parser.get_parameter_dic(request)
        users = userModels.UserInfo.objects.all()
        if 'keyword' in param.keys():
            users = userModels.UserInfo.objects.filter(username__contains=param['keyword'])
            ret['code'] = 2000
        if users:
            total = users.count()
            page = PageNumberPagination()
            # 获取分页数据
            page_data = page.paginate_queryset(queryset=users, request=request, view=self)
            # 序列化  #instance接受queryset对象或者单个model对象，当有多条数据时候，使用many=True,单个对象many=False
            ser = UserSerializer(instance=page_data, many=True)
            # ret_user = json.dumps(ser.data, ensure_ascii=False)
            ret['code'] = 2000
            ret['msg'] = 'success'
            ret['total'] = total
            ret['data'] = ser.data
            print('更新完成', ser.data)

        return JsonResponse(ret)


class UserDetail(APIView):
    authentication_classes = []

    def post(self, request):
        '''
        用户注册
        :param request:
        :return:
        '''
        ret = {
            'code': 1000,
            'msg': None
        }
        data_dic = Parser.get_parameter_dic(request)
        print(data_dic)
        ser = UserSerializer(data=data_dic)
        if ser.is_valid():
            ser.save()
            ret['code'] = 2000
            ret['msg'] = '用户创建成功'
        else:
            ret['code'] = 10001
            ret['msg'] = ser.errors

        return JsonResponse(ret)

    def patch(self, request):
        '''
         用户更新
        :param request:
        :return:
        '''
        ret = {
            'code': 1000,
            'msg': None
        }
        data_dic = Parser.get_parameter_dic(request)
        user = userModels.UserInfo.objects.get(username=data_dic['username'])

        ser = UserSerializer(instance=user, data=data_dic)
        if ser.is_valid():
            ser.save()
            print('更新后',ser.data)
            ret['code'] = 2000
            ret['msg'] = '用户更新成功'
        else:
            ret['code'] = 10001
            ret['msg'] = ser.errors

        return JsonResponse(ret)

    def delete(self, request):
        '''
         删除用户
        :param request:
        :return:
        '''
        ret = {
            'code': 1000,
            'msg': None
        }
        data_dic = Parser.get_parameter_dic(request)
        obj = userModels.UserInfo.objects.filter(username=data_dic['username'])
        if obj:
            obj.delete()
            ret['code'] = 2000
            ret['msg'] = '删除成功'
        return JsonResponse(ret)




