from django.shortcuts import render
from rest_framework.views import APIView, Request
from django.http import JsonResponse, QueryDict
from api import models
import json


# Create your views here.

def md5(user):
    import hashlib
    import time
    # 当前时间，相当于生成一个随机的字符串
    ctime = str(time.time())
    m = hashlib.md5(bytes(user, encoding='utf-8'))
    m.update(bytes(ctime, encoding='utf-8'))
    return m.hexdigest()


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


class Login(APIView):
    def post(self, request):
        ret = {
            'code': 1000,
            'msg': None,
            'data': None
        }
        print('request data: ', request.data)
        try:
            param_dic = get_parameter_dic(request)
            user = param_dic['username']
            password = param_dic['password']
            print('test:::::::', user)
            obj = models.UserInfo.objects.filter(username=user, password=password).first()
            if not obj:
                ret = {
                    'code': 1001,
                    'msg': '用户名或密码错误'
                }
                return JsonResponse(ret)
            ret['code'] = 2000
            ret['msg'] = 'success'
            token = md5(user)
            # 存在就更新, 不存在就创建
            models.UserToken.objects.update_or_create(user=obj, defaults={'token': token})

            user_dic = {
                'token': token,
            }
            ret['data'] = user_dic
        except Exception as e:
            ret['code'] = 1002
            ret['msg'] = '请求异常'
        return JsonResponse(ret)


class GetUserInfo(APIView):
    authentication_classes = []

    def get(self, request):
        print('request data: ', request.data)

        ret = {
            'code': 1000,
            'msg': None,
            'data': None
        }
        param_dic = get_parameter_dic(request)
        print(param_dic)
        token = param_dic['token']
        obj_token = models.UserToken.objects.filter(token=token)
        if not obj_token:
            ret = {
                'code': 50008,
                'msg': 'token无效',
                'data': None
            }
            return JsonResponse(ret)
        ret['code'] = 2000
        ret['msg'] = 'success'
        token_info = models.UserToken.objects.get(token=token)
        print(token_info.user_id)
        user_info = models.UserInfo.objects.get(id=token_info.user_id)
        user_dic = {
            'name': user_info.username,
            'roles': None,
            'avatar': user_info.avatar,
            'introduction': user_info.introduction,
        }
        if user_info.roles == 1:
            user_dic['roles'] = ['admin']
        elif user_info.roles == 2:
            user_dic['roles'] = ['editor']
        else:
            user_dic['roles'] = ['tester']
        ret['data'] = user_dic
        return JsonResponse(ret)


class LoginOut(APIView):
    def post(self, request):
        ret = {
            'code': 1000,
            'msg': None
        }
        param_dic = get_parameter_dic(request)
        token = param_dic['token']
        obj = models.UserToken.objects.filter(token=token)
        if not obj:
            ret['code'] = 50008
            ret['msg'] = 'toekn无效'
            return ret
        models.UserToken.objects.filter(token=token).update(token='')
        ret['code'] = 2000
        ret['msg'] = 'success'
        return JsonResponse(ret)
