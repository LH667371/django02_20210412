from djangoProject.settings import constants

from djangoProject.utils.message import Message
from my_task.main import app


# celery的任务必须定义在tasks文件中，别的文件名不识别
@app.task(name="send_msg")  # name 指定当前异步任务的名称  如果不给，则使用默认的函数名作为任务名
def send_msg(phone, msg):
    """异步发送短信的方法"""
    # message = Message(constants.API_KEY)
    # status = message.send_message(phone, msg)
    # print(status)
    # if status:
    #     print(msg)
    print(msg)
    return "mail"
