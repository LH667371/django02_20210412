from rest_framework.generics import ListAPIView

from home.models import Banner, Nav
from home.serializers import BannerModelSerializer, NavModelSerializer
from djangoProject.settings import constants

# Create your views here.
class BannerListView(ListAPIView):
    """轮播图接口"""
    queryset = Banner.objects.filter(is_show=True, is_delete=False).order_by("orders")[:constants.BANNER_NUM]
    serializer_class = BannerModelSerializer

class HeaderListView(ListAPIView):
    queryset = Nav.objects.filter(is_show=True, is_delete=False, position=1).order_by("orders")
    serializer_class = NavModelSerializer

class FooterListView(ListAPIView):
    queryset = Nav.objects.filter(is_show=True, is_delete=False, position=2).order_by("orders")
    serializer_class = NavModelSerializer