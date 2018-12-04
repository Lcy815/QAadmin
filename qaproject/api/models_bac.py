from django.db import models


# Create your models here.
class UserInfo(models.Model):
    USER_TYPE = (
        (1, 'admin'),
        (2, 'editor'),
        (3, 'tester')
    )

    roles = models.IntegerField(choices=USER_TYPE)
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=64)
    introduction = models.CharField(max_length=64)
    avatar = models.CharField(max_length=128)


class UserToken(models.Model):
    user = models.OneToOneField(UserInfo, on_delete=models.CASCADE)
    token = models.CharField(max_length=64)


