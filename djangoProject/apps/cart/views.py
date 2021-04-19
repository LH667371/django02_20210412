import logging

from django_redis import get_redis_connection
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from course.models import Course

# Create your views here.
log = logging.getLogger("django")


class CartView(ViewSet):
    """购物车视图"""

    # 权限：登录的用户才可以访问
    permission_classes = [IsAuthenticated]
    # 认证用户携带的 jwt token
    authentication_classes = [JSONWebTokenAuthentication]

    def add_cart(self, request):
        """
        将课程添加至购物车的相关操作
        :param request: 用户id  课程id  勾选状态  有效期选项
        :return:
        """
        course_id = request.data.get("course_id")
        user_id = request.user.id
        # print(course_id, user_id)
        # 有效期  为0代表永久有效  其他的代表一定时间内有效
        expire = 0
        try:
            course = Course.objects.get(is_show=True, is_delete=False, pk=course_id)
        except Course.DoesNotExist:
            return Response({"message": "参数有误，课程不存在"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 获取Redis连接
            redis_connection = get_redis_connection("cart")
            # 将购物车数据通过管道保存到redis
            pipeline = redis_connection.pipeline()
            # 开启管道
            pipeline.multi()
            # 商品的信息以及对应的有效期
            pipeline.hset("cart_%s" % user_id, course_id, expire)
            # 被勾选的商品
            pipeline.sadd("select_%s" % user_id, course_id)
            # 将以上两个命令发送到redis执行
            pipeline.execute()

            # 获取购物车中商品的总数量
            course_len = redis_connection.hlen("cart_%s" % user_id)

        except:
            # 将本次错误信息记录到日志中
            log.error("购物车保存数据失败")
            return Response({"message": "购物车添加失败"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"message": "购物车添加成功", "cart_length": course_len})

    def list_cart(self, request):
        """
        返回购物车列表所需的数据
        :param request:
        :return:
        """
        user_id = request.user.id

        redis_connection = get_redis_connection("cart")
        cart_list_byte = redis_connection.hgetall("cart_%s" % user_id)
        select_list_byte = redis_connection.smembers("select_%s" % user_id)

        # print(cart_list_byte, select_list_byte)

        # 循环从数据库中查询出课程的信息
        course_data = []
        for course_id_byte, expire_id_byte in cart_list_byte.items():
            course_id = int(course_id_byte)
            expire_id = int(expire_id_byte)

            try:
                course = Course.objects.get(is_show=True, is_delete=False, pk=course_id)
            except Course.DoesNotExist:
                continue
            if course.course_type == 3:
                price = 0
            else:
                price = course.price
            # 购物车所需的信息
            course_data.append({
                "course_id": course.id,
                "name": course.name,
                # 图片 返回的是图片的显示路径
                "image": course.course_img.url,
                "price": price,
                "selected": True if course_id_byte in select_list_byte else False,
                "expire_id": expire_id
            })

        return Response(course_data)

    def car_course_select(self, request):
        """
        修改购物车列表选中的状态
        :param request:
        :return:
        """
        user_id = request.user.id
        course_id = request.data.get("course_id")
        selected = request.data.get("selected")

        redis_connection = get_redis_connection("cart")
        if selected:
            redis_connection.sadd("select_%s" % user_id, course_id)
        else:
            redis_connection.srem("select_%s" % user_id, course_id)
        return Response('OK')

    def car_all_select(self, request):
        """
        修改购物车列表选中的状态
        :param request:
        :return:
        """
        user_id = request.user.id
        course_id = request.data.get("course_id")
        selected = request.data.get("selected")

        redis_connection = get_redis_connection("cart")
        # 将购物车数据通过管道保存到redis
        pipeline = redis_connection.pipeline()
        # 开启管道
        pipeline.multi()
        if selected:
            for id in course_id:
                pipeline.sadd("select_%s" % user_id, id)
        else:
            for id in course_id:
                redis_connection.srem("select_%s" % user_id, id)
        # 将以上两个命令发送到redis执行
        pipeline.execute()
        return Response('OK')
