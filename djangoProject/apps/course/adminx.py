import xadmin

from course.models import CourseCategory, Course, Teacher, CourseChapter, CourseLesson, Comment, CourseDiscountType, \
    CourseDiscount, CoursePriceDiscount, Activity, CourseExpire


class CourseCategoryModelAdmin(object):
    """课程分类模型管理类"""
    list_display = ['id', 'name']
    ordering = ['id']


xadmin.site.register(CourseCategory, CourseCategoryModelAdmin)


class CourseModelAdmin(object):
    """课程模型管理类"""
    list_display = ['id', 'name', 'course_type', 'level', 'pub_date', 'period', 'file_path', 'status',
                    'course_category', 'students', 'lessons', 'pub_lessons', 'price', 'teacher']
    ordering = ['id']


xadmin.site.register(Course, CourseModelAdmin)


class TeacherModelAdmin(object):
    """老师模型管理类"""
    list_display = ['id', 'name', 'role', 'title', 'signature', 'image']
    ordering = ['id']


xadmin.site.register(Teacher, TeacherModelAdmin)


class CourseChapterModelAdmin(object):
    """章节模型管理类"""
    list_display = ['id', 'name', 'chapter', 'pub_date', 'course', 'orders']
    ordering = ['id']


xadmin.site.register(CourseChapter, CourseChapterModelAdmin)


class CourseLessonModelAdmin(object):
    """课时模型管理类"""
    list_display = ['id', 'name', 'section_type', 'section_link', 'duration', 'pub_date', 'free_trail', 'course',
                    'chapter', 'is_show', 'is_show_list', 'orders']
    ordering = ['id']


xadmin.site.register(CourseLesson, CourseLessonModelAdmin)


class CommentModelAdmin(object):
    list_display = ['id', 'user', 'course', 'date', 'is_delete']
    ordering = ['id']


xadmin.site.register(Comment, CommentModelAdmin)


# 以下是优惠活动相关
class PriceDiscountTypeModelAdmin(object):
    """价格优惠类型"""
    list_display = ['id', 'name', 'remark', 'is_delete']
    ordering = ['id']


xadmin.site.register(CourseDiscountType, PriceDiscountTypeModelAdmin)


class PriceDiscountModelAdmin(object):
    """价格优惠公式"""
    list_display = ['id', 'discount_type', 'condition', 'sale', 'is_delete']
    ordering = ['id']


xadmin.site.register(CourseDiscount, PriceDiscountModelAdmin)


class CoursePriceDiscountModelAdmin(object):
    """商品优惠和活动的关系"""
    list_display = ['id', 'course', 'active', 'discount', 'is_delete']
    ordering = ['id']


xadmin.site.register(CoursePriceDiscount, CoursePriceDiscountModelAdmin)


class ActivityModelAdmin(object):
    """商品活动模型"""
    list_display = ['id', 'name', 'start_time', 'end_time', 'remark', 'is_delete']
    ordering = ['id']


xadmin.site.register(Activity, ActivityModelAdmin)

class CourseExpireModelAdmin(object):
    """商品活动模型"""
    list_display = ['id', 'course', 'expire_time', 'expire_text', 'price', 'is_delete']
    ordering = ['id']


xadmin.site.register(CourseExpire, CourseExpireModelAdmin)
