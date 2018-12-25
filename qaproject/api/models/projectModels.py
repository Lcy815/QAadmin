#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : projectModels.py
# @Author: Lcy
# @Date  : 2018/12/20
# @Desc  : 项目model
from django.db import models
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

class Projects(models.Model):

    id = models.AutoField(primary_key=True)
    pname = models.CharField(max_length=64)
    pintroduction = models.CharField(blank=True, max_length=64)


class Modules(models.Model):

    id = models.AutoField(primary_key=True)
    mname = models.CharField(max_length=64)
    mintroduction = models.CharField(blank=True, max_length=64)
    developer = models.CharField(max_length=32)
    project = models.ForeignKey(Projects, related_name='modules', on_delete=models.CASCADE, blank=True)

class ModuleSerializer(serializers.ModelSerializer):

    pname = serializers.SerializerMethodField()
    class Meta:
        model = Modules
        fields = ('id', 'mname', 'mintroduction', 'developer', 'pname', 'project')

    def get_pname(self, obj):
        return obj.project.pname

class ProjectSerializer(serializers.ModelSerializer):

    modules = ModuleSerializer(many=True, read_only=True)
    pname =serializers.CharField(validators=[UniqueValidator(queryset=Projects.objects.all(), message='用户名重复')])
    class Meta:
        model = Projects
        fields = ('id', 'pname', 'pintroduction', 'modules')



