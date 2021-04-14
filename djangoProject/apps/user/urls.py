from django.urls import path
from rest_framework_jwt import views
from user import views as user_views

urlpatterns = [
    # 通过jwt完成登录
    path('login/', views.obtain_jwt_token),
    path('message_check/', user_views.MessageCheckAPIView.as_view()),
    path('captcha/', user_views.CaptchaAPIView.as_view()),
    path('send_code/', user_views.SendMessageAPIView.as_view()),
    path('register/', user_views.RegisterAPIView.as_view()),
    path('change_pwd/<str:pk>/', user_views.ChangePasswordAPIView.as_view()),
]
