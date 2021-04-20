from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status as http_status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from course.models import CourseCategory, Course, Comment
from course.serializer import CourseCategoryModelSerializer, CourseModelSerializer, CourseInfoModelSerializer, \
    CommentModelSerializer
from course.utils import CoursePageNumberPagination


# Create your views here.

class CourseCategoryView(ListAPIView):
    """课程分类列表"""
    queryset = CourseCategory.objects.filter(is_show=True, is_delete=False).order_by("orders")
    serializer_class = CourseCategoryModelSerializer


class CourseListAPIView(ListAPIView):
    """课程列表"""
    queryset = Course.objects.filter(is_show=True, is_delete=False).order_by("id")
    serializer_class = CourseModelSerializer

    # 指定过滤使用的模板类
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]

    # 指定要搜索的字段
    search_fields = ['id']

    # 指定要过滤的字段
    filter_fields = ("course_category",)

    # 指定排序的条件
    ordering_fields = ("id", "students", "real_price")

    # 指定分页器
    pagination_class = CoursePageNumberPagination


class CourseInfoAPIView(ListAPIView):
    """课程详情"""
    queryset = Course.objects.filter(is_show=True, is_delete=False)
    serializer_class = CourseInfoModelSerializer

    # 指定过滤使用的模板类
    filter_backends = [SearchFilter]

    # 指定要搜索的字段
    search_fields = ['id']


class getCommentAPIView(GenericAPIView):
    def get(self, request, *args, **kwargs):
        comment = Comment.objects.filter(is_delete=False, course=request.GET.get('course')).order_by('-date')
        return Response({
            'results': CommentModelSerializer(comment, many=True).data
        })


class CommentAPIView(GenericAPIView,
                     CreateModelMixin):
    """课程评论"""
    # 登录用户才可以访问
    permission_classes = [IsAuthenticated]
    # 认证用户携带的 jwt token
    authentication_classes = [JSONWebTokenAuthentication]
    # 获取当前视图类要操作的模型
    queryset = Comment.objects.all()
    # 指定当前视图要使用的序列化器类
    serializer_class = CommentModelSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        try:
            comment = Comment.objects.get(id=request.data.get('id'), course=request.data.get('course'))
            comment.is_delete = True
            comment.save()
            return Response({
                'status': 200,
                'results': 'ok',
            })
        except:
            return Response({'message': "删除失败！"}, status=http_status.HTTP_400_BAD_REQUEST)
