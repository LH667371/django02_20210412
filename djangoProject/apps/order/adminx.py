import xadmin

from order import models


class OrderModelAdmin(object):
    list_display = ['id', 'order_number', 'user', 'order_title', 'total_price', 'real_price', 'order_status', 'pay_type',
                    'credit', 'coupon', 'order_desc', 'pay_time', 'is_delete']
    ordering = ['id']


xadmin.site.register(models.Order, OrderModelAdmin)

class OrderDetailModelAdmin(object):
    list_display = ['id', 'order', 'course', 'expire', 'price', 'real_price', 'discount_name', 'is_delete']
    ordering = ['id']
xadmin.site.register(models.OrderDetail, OrderDetailModelAdmin)
