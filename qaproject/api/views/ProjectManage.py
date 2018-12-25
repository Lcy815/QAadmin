#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : ProjectManage.py
# @Author: Lcy
# @Date  : 2018/12/20
# @Desc  : 项目管理

from rest_framework.views import APIView
from django.http import JsonResponse
from ..utils.parser import Parser
from rest_framework.pagination import PageNumberPagination
from ..models.projectModels import Projects, Modules, ProjectSerializer, ModuleSerializer



class Project(APIView):
    authentication_classes = []
    def get(self, request):
        ret = {
            'code': 1000,
            'msg': None,
            'data': []
        }
        obj = Projects.objects.all()
        param_dic = Parser.get_parameter_dic(request)
        if 'keyword' in param_dic.keys():
            obj = Projects.objects.filter(pname__contains=param_dic['keyword'])
        if obj:
            pser = ProjectSerializer(instance=obj, many=True)
            ret['code'] = 2000
            ret['msg'] = 'success'
            ret['data'] = pser.data

        return JsonResponse(ret)

    def post(self, request):
        ret = {
            'code': 1000,
            'msg': None
        }
        param_dic = Parser.get_parameter_dic(request)
        pser = ProjectSerializer(data=param_dic)
        if pser.is_valid():
            pser.save()
            ret['code'] = 2000
            ret['msg'] = 'success'
        else:
            ret['msg'] = pser.errors
        return JsonResponse(ret)

    def patch(self, request):
        ret = {
            'code': 1000,
            'msg': None
        }
        param_dic = Parser.get_parameter_dic(request)
        pro = Projects.objects.get(pname=param_dic['pname'])
        pser = ProjectSerializer(instance=pro, data=param_dic)
        if pser.is_valid():
            pser.save()
            print(pser.data)
            ret['code'] = 2000
            ret['msg'] = '更新成功'
        else:
            ret['msg'] = pser.errors

        return JsonResponse(ret)

    def delete(self, request):
        ret = {
            'code': 1000,
            'msg': None
        }
        param_dic = Parser.get_parameter_dic(request)
        obj = Projects.objects.filter(pname=param_dic['pname'])
        if obj:
            obj.delete()
            ret['code'] = 2000
            ret['msg'] = '删除成功'

        return JsonResponse(ret)

class Module(APIView):

    authentication_classes = []

    def get(self, request):
        ret = {
            'code': 1000,
            'msg': None,
            'total': 0,
            'data': []
        }
        obj = Modules.objects.all()
        if obj:
            mser = ModuleSerializer(instance=obj, many=True)
            ret['code'] = 2000
            ret['msg'] = 'success'
            ret['data'] = mser.data
            ret['total'] = obj.count()
        return JsonResponse(ret)

    def post(self, request):
        ret = {
            'code': 1000,
            'msg': None
        }
        param_dic = Parser.get_parameter_dic(request)
        mser = ModuleSerializer(data=param_dic)
        if mser.is_valid():
            mser.save()
            ret['code'] = 2000
            ret['msg'] = 'success'
        else:
            ret['msg'] = mser.errors

        return JsonResponse(ret)

    def patch(self, request):
        ret = {
            'code': 1000,
            'msg': None
        }
        param_dic = Parser.get_parameter_dic(request)
        mod = Modules.objects.get(id=param_dic['id'])
        mser = ModuleSerializer(instance=mod, data=param_dic)
        if mser.is_valid():
            mser.save()
            ret['code'] = 2000
            ret['msg'] = '更新成功'
        else:
            ret['msg'] = mser.errors

        return JsonResponse(ret)

    def delete(self, request):
        ret = {
            'code': 1000,
            'msg': '系统错误'
        }
        param_dic = Parser.get_parameter_dic(request)
        mod = Modules.objects.filter(id=param_dic['id'])
        if mod:
            mod.delete()
            ret['code'] = 2000
            ret['msg'] = '删除成功'

        return JsonResponse(ret)
