from django.urls import path

from app import views

urlpatterns=[
    path("user/",views.user),
    #类视图url的定义
    path("users/",views.UserView.as_view()),
    # 匹配携带参数的路由
    path("users/<str:pk>/",views.UserView.as_view()),
    path("api_user/",views.UserAPIView.as_view()),
    path("stu/",views.StudentAPIView.as_view()),
]