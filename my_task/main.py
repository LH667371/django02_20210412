import os

import django
from celery import Celery

# 创建celery实例对象
app = Celery('sms')

# celery与Django结合使用  识别并加载django的配置文件
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoProject.settings.develop")
django.setup()

# 通过创建的实例对象加载配置
app.config_from_object("my_task.config")

# 将任务添加至celery的实例对象中
# 自动找到该目录下的tasks文件中的任务去执行
app.autodiscover_tasks(["my_task.sms", 'my_task.order'])

# 启动celery  会根据定义好的配置执行异步任务 不配置Django运行时才需执行
# 在项目的根目录下执行该命令
# celery -A my_task.main worker --loglevel=info