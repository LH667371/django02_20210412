import xadmin

from payments import models


class UserCourseModelAdmin(object):
    list_display = ['id', 'user', 'course', 'trade_no', 'buy_type', 'pay_time', 'out_time', 'is_delete']
    ordering = ['id']


xadmin.site.register(models.UserCourse, UserCourseModelAdmin)
