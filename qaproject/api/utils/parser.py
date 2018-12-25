#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : parser.py
# @Author: Lcy
# @Date  : 2018/12/5
# @Desc  : 解析请求头
from rest_framework.views import Request
from django.http import QueryDict


class Parser:

    def get_parameter_dic(request, *args, **kwargs):
        '''
        解析post请求参数
        :param request:
        :param args:
        :param kwargs:
        :return: 返回字典参数
        '''
        if isinstance(request, Request) == False:
            return {}
        query_params = request.query_params
        if isinstance(query_params, QueryDict):
            query_params = query_params.dict()
        result_data = request.data
        if isinstance(result_data, QueryDict):
            result_data = result_data.dict()

        if query_params != {}:
            return query_params
        else:
            return result_data
