from home import views
from django.urls import path

urlpatterns = [
    path('banner/', views.BannerListView.as_view()),
    path('header/', views.HeaderListView.as_view()),
    path('footer/', views.FooterListView.as_view()),
]
