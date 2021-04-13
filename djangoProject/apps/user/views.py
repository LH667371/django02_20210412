from django.http import HttpResponse
from rest_framework import status as http_status
from rest_framework.response import Response
from rest_framework.views import APIView

from djangoProject.libs.geetest import GeetestLib
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
        result = {"status": "success"} if result else {"status": "fail"}
        return HttpResponse(result)
