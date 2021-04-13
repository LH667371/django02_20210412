from home import views
from django.urls import path
from rest_framework_jwt import views

urlpatterns = [
    # 通过jwt完成登录
    path('login/', views.obtain_jwt_token),
]
