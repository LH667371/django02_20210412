from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from order.models import Order
from order.serializers import OrderModelSerializer, GetOrderModelSerializer, CancelOrderModelSerializer


# Create your views here.

class OrderAPIView(CreateAPIView):
    # 权限：登录的用户才可以访问
    permission_classes = [IsAuthenticated]
    # 认证用户携带的 jwt token
    authentication_classes = [JSONWebTokenAuthentication]
    """订单的视图"""
    queryset = Order.objects.filter(is_delete=False, is_show=True)
    serializer_class = OrderModelSerializer


class GetOrderAPIView(APIView):
    # 权限：登录的用户才可以访问
    permission_classes = [IsAuthenticated]
    # # 认证用户携带的 jwt token
    authentication_classes = [JSONWebTokenAuthentication]
    """订单的视图"""

    def get(self, request, *args, **kwargs):
        user_id = request.GET.get('user')
        order = Order.objects.filter(user_id=user_id)
        serializer = GetOrderModelSerializer(order, many=True)
        return Response(serializer.data)


class CancelOrderAPIView(UpdateAPIView):
    # 权限：登录的用户才可以访问
    # permission_classes = [IsAuthenticated]
    # 认证用户携带的 jwt token
    # authentication_classes = [JSONWebTokenAuthentication]
    """订单的视图"""
    queryset = Order.objects.filter(is_delete=False, is_show=True)
    serializer_class = CancelOrderModelSerializer
