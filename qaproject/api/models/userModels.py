from django.db import models
from rest_framework import serializers

# Create your models here.
class UserInfo(models.Model):
    class Meta:
        app_label = 'api'
    USER_TYPE = (
        (1, 'admin'),
        (2, 'editor'),
        (3, 'tester')
    )

    roles = models.IntegerField(choices=USER_TYPE)
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=64)
    introduction = models.CharField(max_length=64, blank=True)
    avatar = models.CharField(max_length=128, blank=True)
    email = models.EmailField(blank=True)




class UserToken(models.Model):
    class Meta:
        app_label = 'api'
    createtime = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(UserInfo, on_delete=models.CASCADE)
    token = models.CharField(max_length=64)


