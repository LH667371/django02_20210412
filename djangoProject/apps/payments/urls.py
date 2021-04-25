from django.urls import path

from payments import views

urlpatterns = [
    path("pay/", views.ALiPayAPIView.as_view()),
    path("result/", views.PayResultAPIView.as_view()),
]
