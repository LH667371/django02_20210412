from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from order.serializers import OrderModelSerializer
from rest_framework.generics import CreateAPIView

from order.models import Order


# Create your views here.

class OrderAPIView(CreateAPIView):
    # 权限：登录的用户才可以访问
    permission_classes = [IsAuthenticated]
    # 认证用户携带的 jwt token
    authentication_classes = [JSONWebTokenAuthentication]
    """订单的视图"""
    queryset = Order.objects.filter(is_delete=False, is_show=True)
    serializer_class = OrderModelSerializer
