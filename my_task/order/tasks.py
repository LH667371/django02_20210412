import datetime

from my_task.main import app
from order.models import Order


# celery与Django结合使用  识别并加载django的配置文件


@app.task(name="check_order")
def check_order():
    """未支付订单超时取消"""
    print('正在运行 未支付订单超时取消 任务')
    order = Order.objects.filter(create_time__lt=datetime.datetime.now() - datetime.timedelta(hours=1))
    print(order)
    for i in order:
        if datetime.datetime.now() - i.create_time > datetime.timedelta(minutes=1) and i.order_status == 0:
            change = Order.objects.get(pk=i.id)
            change.order_status = 3
            change.save()

if __name__ == '__main__':
    check_order()