import requests
from djangoProject.settings import constants

class Message(object):

    def __init__(self, api_key):
        # 账号的唯一标识
        self.api_key = api_key
        # 发送单条短信使用的接口
        self.single_send_url = "https://sms.yunpian.com/v2/sms/single_send.json"

    def send_message(self, phone, code):
        """
        短信发送的实现
        :param phone: 要接收短信的手机号
        :param code: 随机验证码
        """
        params = {
            "apikey": self.api_key,
            "mobile": phone,
            "text": "【毛信宇test】您的验证码是{code}。如非本人操作，请忽略本短信".format(code=code)
        }

        # 发送post请求
        req = requests.post(self.single_send_url, data=params)
        # 200代表发送成功  200以外都是失败
        print(req)


if __name__ == '__main__':
    message = Message(constants.API_KEY)
    message.send_message("手机号", "code验证码")