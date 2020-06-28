from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import User


@csrf_exempt
def user(request):
    if request.method=="GET":
        print("GET success 查询")
        #查询 用户的相关逻辑
        return HttpResponse("GET success")
    elif request.method =="POST":
        print("POST success 添加")
        # 添加用户相关逻辑
        return HttpResponse("POST success")
    elif request.method == "PUT":
        print("PUT success 修改")
        return HttpResponse("PUT success")
    elif request.method =="DELETE":
        print("DELETE success 删除")
        return HttpResponse("DELETE success")

@method_decorator(csrf_exempt,name="dispatch")  #让类视图免除crsf认证
class UserView(View):
    """
    类视图内部通过请求的方法来匹配到对应的内部的函数，从而进行对应的处理
    """
    def get(self,request,*args,**kwargs):
        #获取用户的id
        # user_id=request.GET.get("user_id")
        user_id=kwargs.get("pk")
        print(user_id)
        if user_id:
            # 如果查询出对应的用户信息，则将用户的信息返回到前端
            user_val=User.objects.filter(pk=user_id).values("username","password","gender").first()
            if user_val:
                return JsonResponse({
                    "status":200,
                    "message":"查询单个用户成功",
                    "results":user_val
                })
        else:
            # 如果没有传参数id代表查询所有
            user_list=User.objects.all().values("username","password","gender")
            print(type(user_list))
            if user_list:
                return JsonResponse({
                    "status":200,
                    "message":"查询所有用户成功",
                    "results":list(user_list),
                })
        return JsonResponse({
            "status":500,
            "message":"查询失败",
        })

    def post(self, request, *args, **kwargs):
        """
        新增单个用户
        """
        username = request.POST.get("username")
        pwd = request.POST.get("password")
        try:
            user_obj = User.objects.create(username=username, password=pwd)
            return JsonResponse({
                "status": 201,
                "message": "创建用户成功",
                "results": {"username": user_obj.username, "gender": user_obj.gender}
            })
        except:
            return JsonResponse({
                "status": 500,
                "message": "创建用户失败",
            })
    def put(self,request,*args,**kwargs):
        user_id = kwargs.get("pk")
        user_list = User.objects.all().values("username", "password", "gender")
        username=request.POST.get("username")
        print(username)
        user_obj=User.objects.filter(pk=user_id)
        if user_obj:
            user_obj.username=username
            user_obj.save()
            return JsonResponse({
                "status": 200,
                "message": "修改用户信息成功",
                "results": list(user_list)
            })
        # 查询 用户的相关逻辑
        return HttpResponse("put success")
    def delete(self,request,*args,**kwargs):
        user_id = kwargs.get("pk")
        user_list = User.objects.all().values("username", "password", "gender")
        print(user_id)
        try:
            if user_id:
                user_obj=User.objects.filter(pk=user_id)
                user_obj.delete()
                return JsonResponse({
                    "status":200,
                    "message":"删除用户成功",
                    "results":list(user_list)
                })
        except:
            return JsonResponse({
                "status":500,
                "message":"删除用户失败",
            })

#开发基于drf的视图
class UserAPIView(APIView):
    def get(self,request,*args,**kwargs):
        # 可以通过_request 访问Django原生的request对象
        print(request._request.GET)
        # 通过DRF 的request对象获取参数
        print(request.GET)
        # 通过quer_params来获取参数
        print(request.query_params)
        return Response("drf get success")
    def post(self,request,*args,**kwargs):
        # post请求传递参数的形式  form-data  www-urlencoded  json
        print(request._request.POST)  # Django 原生的request对象
        print(request.POST)  # DRF 封装后的request对象
        # 可以获取多种格式的参数 DRF 扩展的请回去参数  兼容性最强
        print(request.data)
        return Response("drf post success")
