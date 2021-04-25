from django.urls import path

from order import views

urlpatterns = [
    path("option/", views.OrderAPIView.as_view()),
    path("get_option/", views.GetOrderAPIView.as_view()),
    path("cancel_option/<str:pk>/", views.CancelOrderAPIView.as_view()),
]
