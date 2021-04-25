from my_task.main import app

@app.task(name="check_order")
def check_order():
    """未支付订单超时取消"""
    print('正在运行 未支付订单超时取消 任务')
    pass