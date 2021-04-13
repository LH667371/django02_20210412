from django.urls import path
from rest_framework_jwt import views
from user import views as user_views

urlpatterns = [
    # 通过jwt完成登录
    path('login/', views.obtain_jwt_token),
    path('captcha/', user_views.CaptchaAPIView.as_view()),
]
