from django.urls import path

from course import views

urlpatterns = [
    # 通过jwt完成登录
    path('category/', views.CourseCategoryView.as_view()),
    path("list/", views.CourseListAPIView.as_view()),
    path("info/", views.CourseInfoAPIView.as_view()),
    path("comment/", views.CommentAPIView.as_view()),
]
