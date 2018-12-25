from django.shortcuts import render
from rest_framework.views import APIView, Request
from django.http import JsonResponse, QueryDict
from api.models import userModels
from ..utils.parser import Parser

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
    authentication_classes = []
    def post(self, request):
        ret = {
            'code': 1000,
            'msg': None,
            'data': None
        }
        print('request data: ', request.META.get('HTTP_ADMIN_TOKEN'))
        try:
            param_dic = get_parameter_dic(request)
            user = param_dic['username']
            password = param_dic['password']
            obj = userModels.UserInfo.objects.filter(username=user, password=password).first()
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
            userModels.UserToken.objects.update_or_create(user=obj, defaults={'token': token})

            user_dic = {
                'token': token,
            }
            ret['data'] = user_dic
        except Exception as e:
            ret['code'] = 1002
            ret['msg'] = '请求异常'
        return JsonResponse(ret)


class GetUserInfo(APIView):

    def get(self, request):
        print('header', request.META.get('HTTP_X_CSRFTOKEN'))
        ret = {
            'code': 1000,
            'msg': None,
            'data': None
        }
        param_dic = get_parameter_dic(request)
        token = param_dic['token']
        obj_token = userModels.UserToken.objects.filter(token=token)
        if not obj_token:
            ret = {
                'code': 50008,
                'msg': 'token无效',
                'data': None
            }
            return JsonResponse(ret)
        ret['code'] = 2000
        ret['msg'] = 'success'
        token_info = userModels.UserToken.objects.get(token=token)
        user_info = userModels.UserInfo.objects.get(id=token_info.user_id)
        user_dic = {
            'name': user_info.username,
            'roles': None,
            'avatar': user_info.avatar,
            'introduction': user_info.introduction,
        }
        roles_list = []
        if user_info.roles == 1:
            roles_list.append('admin')
        elif user_info.roles == 2:
            roles_list.append('editor')
        else:
            roles_list.append('tester')
        user_dic['roles'] = roles_list
        ret['data'] = user_dic
        return JsonResponse(ret)


class LoginOut(APIView):
    authentication_classes = []
    def post(self, request):
        ret = {
            'code': 1000,
            'msg': None
        }
        param_dic = get_parameter_dic(request)
        token = param_dic['token']
        obj = userModels.UserToken.objects.filter(token=token)
        if not obj:
            ret['code'] = 50008
            ret['msg'] = 'toekn无效'
            return JsonResponse(ret)
        userModels.UserToken.objects.filter(token=token).update(token='')
        ret['code'] = 2000
        ret['msg'] = 'success'
        return JsonResponse(ret)
