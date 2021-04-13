from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from user.models import UserInfo


def jwt_response_payload_handler(token, user=None, request=None):
    """
    重写jwt返回的数据
    :param token: 签发的token
    :param user: 登录用户的数据
    :param request: 发送的请求
    :return: token, user.username, user.id
    """
    return {
        'token': token,
        'username': user.username,
        'user_id': user.id,
    }


def get_user_by_account(account):
    """
    根据账户查找对应的用户
    :param account: 用户名，邮箱，手机号
    :return: UserInfo对象 或者 None
    """
    try:
        user = UserInfo.objects.filter(Q(username=account) | Q(phone=account) | Q(email=account)).first()
    except UserInfo.DoesNotExist:
        return None
    else:
        return user

class UserModelBackend(ModelBackend):
    """重写django的登录逻辑"""
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        :param request:
        :param username: 用户名
        :param password: 密码
        :param kwargs:
        :return: UserInfo对象 或者 None
        """
        user = get_user_by_account(username)

        if user and user.check_password(password) and user.is_authenticated:
            return user
        else:
            return None