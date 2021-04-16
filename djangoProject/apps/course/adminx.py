import xadmin

from course.models import CourseCategory, Course, Teacher, CourseChapter, CourseLesson


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
