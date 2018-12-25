#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : pagination.py
# @Author: Lcy
# @Date  : 2018/12/14
# @Desc  : 自定义分页
from rest_framework.pagination import PageNumberPagination


class MyPageNumberPagination(PageNumberPagination):
    page_size = 10
    pass
