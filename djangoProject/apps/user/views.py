from django.http import HttpResponse
from djangoProject.settings import constants
from django_redis import get_redis_connection
from rest_framework import status as http_status
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from djangoProject.libs.geetest import GeetestLib
from djangoProject.utils.generate_code import generate_code
from user.models import UserInfo
from user.serializer import RegisterSerializers, ChangePasswordSerializers
from user.utils import get_user_by_account

# Create your views here.

# 请在官网申请ID使用，示例ID不可使用
pc_geetest_id = "eceb3f15b58977f4ccbf2680069aa19d"
pc_geetest_key = "2193c33833d27bf218e80d400618f525"


class CaptchaAPIView(APIView):
    """极验验证码视图类"""
    status = False

    def get(self, request):
        username = request.query_params.get('username')
        user = get_user_by_account(username)
        if not user:
            return Response({"msg": "用户不存在"}, status=http_status.HTTP_400_BAD_REQUEST)
        # 构建一个验证码对象
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        self.status = gt.pre_process(user.id)
        # 响应获取的数据
        response_str = gt.get_response_str()
        return HttpResponse(response_str)

    def post(self, request):
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        challenge = request.data.get(gt.FN_CHALLENGE, '')
        validate = request.data.get(gt.FN_VALIDATE, '')
        seccode = request.data.get(gt.FN_SECCODE, '')
        username = request.data.get('username')
        user = get_user_by_account(username)
        if user:
            result = gt.success_validate(challenge, validate, seccode, user.id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)
        result = {'status': 'success'} if result else {'status': 'fail'}
        return HttpResponse(result)


class RegisterAPIView(CreateAPIView):
    """注册视图"""
    queryset = UserInfo.objects.all()
    serializer_class = RegisterSerializers


class SendMessageAPIView(APIView):
    """短信验证码"""

    def get(self, request):
        """
        根据提供的手机号来发送验证码
        :param request:
        """
        phone = request.query_params.get('phone')
        status = request.query_params.get('status')
        if status == 'login' or status == 'forgot':
            user = UserInfo.objects.filter(phone=phone)
            if not user:
                return Response({'message': '您未注册！是否跳转去注册？'}, status=http_status.HTTP_400_BAD_REQUEST)
        elif status == 'register':
            user = UserInfo.objects.filter(phone=phone)
            if user:
                return Response({'message1': '您已经注册！是否跳转去登录？'})
        # 获取redis链接
        redis_connection = get_redis_connection('sms_code')
        # 1. 判断该手机号格式以及是否在60s内发送过验证码
        phone_code = redis_connection.get('sms_%s' % phone)
        # 2. 生成随机验证码
        if phone_code:
            return Response({'message': "您已经在60s内发送过验证码了！"}, status=http_status.HTTP_401_UNAUTHORIZED)
        code = generate_code()
        # 3. 将验证码保存redis中
        redis_connection.setex('sms_%s' % phone, constants.SMS_EXPIRE_TIME, code)
        redis_connection.setex('mobile_%s' % phone, constants.MOBILE_EXPIRE_TIME, code)
        redis_connection.delete("count%s" % phone)
        print(code)
        # 4. 调用发送短信方法，完成发送
        # message = Message(constants.API_KEY)
        # status = message.send_message(phone, code)
        # print(status)
        # 5. 响应发送的结果
        return Response({'message': '发送短信成功'})


class MessageCheckAPIView(APIView):
    """验证码登录视图"""

    def post(self, request):
        phone = request.data.get('phone')
        code = request.data.get('code')
        status = request.data.get('status')
        # 验证用户提交的验证码是否正确
        from django_redis import get_redis_connection
        connection = get_redis_connection("sms_code")
        redis_code = connection.get("mobile_%s" % phone)

        if redis_code.decode() != code:
            count = connection.get("count%s" % phone)
            if count:
                connection.set("count%s" % phone, int(count.decode()) + 1)
            else:
                connection.set("count%s" % phone, 1)
            if int(connection.get("count%s" % phone).decode()) > 5:
                connection.delete("mobile_%s" % phone)
                connection.delete("sms_%s" % phone)
                connection.delete("count%s" % phone)
                return Response({'message': "检测输入验证码多次不正确，请重新获取！"}, status=http_status.HTTP_400_BAD_REQUEST)
            return Response({'message': "验证码不正确！"}, status=http_status.HTTP_400_BAD_REQUEST)
        connection.delete("mobile_%s" % phone)
        connection.delete("sms_%s" % phone)
        connection.delete("count%s" % phone)
        user = UserInfo.objects.get(phone=phone)
        from rest_framework_jwt.settings import api_settings
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        if status == 'login':
            return Response({'token': token, 'username': user.username, 'user_id': user.id})
        else:
            return Response({'token_change': token, 'user_id': user.id})


class ChangePasswordAPIView(GenericAPIView, UpdateModelMixin):
    """修改视图"""
    # # 登录用户才可以访问
    permission_classes = [IsAuthenticated]
    # 认证用户携带的 jwt token
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = UserInfo.objects.all()
    serializer_class = ChangePasswordSerializers

    def patch(self, request, *args, **kwargs):
        self.partial_update(request, *args, **kwargs)
        return Response({'message': "密码修改成功，快去登录吧！"})
