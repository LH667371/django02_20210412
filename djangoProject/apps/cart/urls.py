from django.urls import path

from cart import views

urlpatterns = [
    path("option/", views.CartView.as_view({'post': 'add_cart', 'get': 'list_cart', 'patch': 'car_course_select', 'put': 'car_all_select', 'delete': 'del_car'})),
]
