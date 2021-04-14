import random
import re
import string

from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from user.models import UserInfo
from user.utils import get_user_by_account


class RegisterSerializers(ModelSerializer):
    sms_code = serializers.CharField(min_length=4, max_length=6, required=True, write_only=True)
    token = serializers.CharField(max_length=1024, read_only=True, help_text="返回前端的token")

    class Meta:
        model = UserInfo
        fields = ("phone", "password", "id", "username", "token", "sms_code")

        extra_kwargs = {
            "phone": {
                "write_only": True
            },
            "password": {
                "write_only": True
            },
            "id": {
                "read_only": True
            },
            "username": {
                "read_only": True
            },

        }

    def validate(self, attrs):
        """验证用户提交的注册信息是否合法"""
        phone = attrs.get("phone")
        password = attrs.get("password")
        code = attrs.get("sms_code")

        # 验证手机号的格式
        if not re.match(r'^1([358][0-9]|4[01456879]|6[2567]|7[0-8]|9[0-3,5-9])\d{8}$', phone):
            raise serializers.ValidationError("手机号格式有误！")

        # 验证手机号是否被注册了
        try:
            user = get_user_by_account(account=phone)
        except:
            user = None
        if user:
            raise serializers.ValidationError("当前手机号已经被注册!")

        # 验证密码格式
        if not re.match(r'^(?![0-9]+$)(?![a-z]+$)(?![A-Z]+$)(?!([^(0-9a-zA-Z)])+$).{6,20}$', password):
            raise serializers.ValidationError("密码格式有误！")

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
                raise serializers.ValidationError("检测输入验证码多次不正确，请重新获取！")
            raise serializers.ValidationError("验证码不正确！")
        # 为了防止破解  同一个验证吗可以只允许验证5次
        return attrs

    def create(self, validated_data):
        """
        重写create方法，完成对象的保存  token的生成
        :param validated_data:
        :return: username id  token
        """
        phone = validated_data.get("phone")
        password = validated_data.get("password")

        # 设置默认用户名 密码加密
        username = ''.join(random.sample(string.digits + string.ascii_letters + string.punctuation,
                                         random.randint(2, 6))) + phone + ''.join(
            random.sample(string.digits + string.ascii_letters + string.punctuation, random.randint(2, 4)))
        hash_pwd = make_password(password)
        try:
            id = UserInfo.objects.values('id').last()['id'] + 1
        except:
            id = 1
        # 保存对象
        user = UserInfo.objects.create(id=id, phone=phone, username=username, password=hash_pwd)

        # 用户创建后为该用户生成token
        if user:
            from rest_framework_jwt.settings import api_settings
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            # 确认注册成功删除redis字段
            from django_redis import get_redis_connection
            connection = get_redis_connection("sms_code")
            connection.delete("mobile_%s" % phone)
            connection.delete("sms_%s" % phone)
            connection.delete("count%s" % phone)
            payload = jwt_payload_handler(user)
            user.token = jwt_encode_handler(payload)
        return user

class ChangePasswordSerializers(ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ["password"]

    def validate(self, attrs):
        password = attrs.get('password')
        # 验证密码格式
        if not re.match(r'^(?![0-9]+$)(?![a-z]+$)(?![A-Z]+$)(?!([^(0-9a-zA-Z)])+$).{6,20}$', password):
            raise serializers.ValidationError("密码格式有误！")
        else:
            attrs['password'] = make_password(password)
        return attrs
