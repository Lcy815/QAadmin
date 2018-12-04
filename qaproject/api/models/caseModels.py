#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : caseModels.py
# @Author: Lcy
# @Date  : 2018/11/30
# @Desc  : caseModels

from django.db import models

class CaseInfo(models.Model):

    class Meta:
        app_label = 'api'
    case_id = models.IntegerField()
    case_name = models.CharField(max_length=128)
