from functools import reduce

from django.db import models

from djangoProject.utils.generl_model import BaseModel
# Create your models here.
from user.models import UserInfo


class CourseCategory(BaseModel):
    """课程分类"""
    name = models.CharField(max_length=64, unique=True, verbose_name="分类名称")

    class Meta:
        db_table = "course_category"
        verbose_name = "课程分类"
        verbose_name_plural = "课程分类"

    def __str__(self):
        return "%s" % self.name


class Course(BaseModel):
    """专题课程"""
    course_type = (
        (0, '收费课程'),
        (1, '高级课程'),
        (2, '专业技能'),
        (3, '限时免费')
    )
    level_choices = (
        (0, '入门'),
        (1, '进阶'),
        (2, '大师'),
    )
    status_choices = (
        (0, '上线'),
        (1, '下线'),
        (2, '预上线'),
    )
    name = models.CharField(max_length=128, verbose_name="课程名称")
    course_img = models.ImageField(upload_to="course", max_length=255, verbose_name="封面图片", blank=True, null=True)
    course_video = models.FileField(upload_to="video", null=True, blank=True, verbose_name="封面视频")
    course_type = models.SmallIntegerField(choices=course_type, default=0, verbose_name="付费类型")
    # 使用这个字段的原因
    brief = models.TextField(max_length=2048, verbose_name="详情介绍", null=True, blank=True)
    level = models.SmallIntegerField(choices=level_choices, default=1, verbose_name="难度等级")
    pub_date = models.DateField(verbose_name="发布日期", auto_now_add=True)
    period = models.IntegerField(verbose_name="建议学习周期(day)", default=7)
    file_path = models.FileField(max_length=128, verbose_name="课件路径", blank=True, null=True)
    status = models.SmallIntegerField(choices=status_choices, default=0, verbose_name="课程状态")
    course_category = models.ForeignKey("CourseCategory", on_delete=models.CASCADE, null=True, blank=True,
                                        verbose_name="课程分类")
    students = models.IntegerField(verbose_name="学习人数", default=0)
    lessons = models.IntegerField(verbose_name="总课时数量", default=0)
    pub_lessons = models.IntegerField(verbose_name="课时更新数量", default=0)
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="课程原价", default=0)
    teacher = models.ForeignKey("Teacher", on_delete=models.DO_NOTHING, null=True, blank=True, verbose_name="授课老师")

    @property
    def lesson_list(self):
        """
        返回该课程的前四个课时
        用于课程列表页面展示课时
        # 先查当前课程的章节  再通过章节查找课时
        """
        # 获取属于当前课程的所有课时
        lesson_list = CourseLesson.objects.filter(is_show=True, is_delete=False, course_id=self.id).all()
        data_list = []
        for lesson in lesson_list:
            data_list.append({
                'orders': lesson.orders,
                'chapter': lesson.chapter.chapter,
                'name': lesson.name,
                'free_trail': lesson.free_trail
            })
        return data_list

    @property
    def lesson_info(self):
        """
        返回该课程的前四个课时
        用于课程列表页面展示课时
        # 先查当前课程的章节  再通过章节查找课时
        """
        # 获取属于当前课程的所有课时
        lesson_list = CourseLesson.objects.filter(is_show_list=True, is_delete=False, course_id=self.id).all()
        data_list = []
        for lesson in lesson_list:
            data_list.append({
                'chapter': lesson.chapter.chapter,
                'chapter_name': lesson.chapter.name,
            })
        data_list = reduce(lambda x, y: x if y in x else x + [y], [[], ] + data_list)
        for i in range(len(data_list)):
            list1 = []
            for lesson in lesson_list:
                if lesson.chapter.chapter == data_list[i]['chapter']:
                    list1.append({
                        'lesson_orders': lesson.orders,
                        'name': lesson.name,
                        'free_trail': lesson.free_trail,
                        'duration': lesson.duration,
                        'Lesson_video': str(lesson.lesson_video),
                    })
            data_list[i]['lesson'] = list1
        return data_list

    @property
    def type(self):
        return self.get_course_type_display()

    @property
    def level_n(self):
        return self.get_level_display()

    class Meta:
        db_table = "course"
        verbose_name = "专题课程"
        verbose_name_plural = "专题课程"

    def __str__(self):
        return "%s" % self.name


class Teacher(BaseModel):
    """讲师、导师表"""
    role_choices = (
        (0, '讲师'),
        (1, '班主任'),
        (2, '教学总监'),
    )
    name = models.CharField(max_length=32, verbose_name="讲师title")
    role = models.SmallIntegerField(choices=role_choices, default=0, verbose_name="讲师身份")
    title = models.CharField(max_length=64, verbose_name="职称")
    signature = models.CharField(max_length=255, verbose_name="导师签名", help_text="导师签名", blank=True, null=True)
    image = models.ImageField(upload_to="teacher", null=True, verbose_name="讲师封面")
    brief = models.TextField(max_length=1024, verbose_name="讲师描述")

    @property
    def role_name(self):
        return self.get_role_display()

    class Meta:
        db_table = "teacher"
        verbose_name = "讲师导师"
        verbose_name_plural = "讲师导师"

    def __str__(self):
        return "%s" % self.name


class CourseChapter(BaseModel):
    """课程章节"""
    course = models.ForeignKey("Course", related_name='coursechapters', on_delete=models.CASCADE, verbose_name="课程名称")
    chapter = models.SmallIntegerField(verbose_name="第几章", default=1)
    name = models.CharField(max_length=128, verbose_name="章节标题")
    summary = models.TextField(verbose_name="章节介绍", blank=True, null=True)
    pub_date = models.DateField(verbose_name="发布日期", auto_now_add=True)

    class Meta:
        db_table = "course_chapter"
        verbose_name = "课程章节"
        verbose_name_plural = "课程章节"

    def __str__(self):
        return "%s:(第%s章)%s" % (self.course, self.chapter, self.name)


class CourseLesson(BaseModel):
    """课程课时"""
    section_type_choices = (
        (0, '文档'),
        (1, '练习'),
        (2, '视频')
    )
    chapter = models.ForeignKey("CourseChapter", related_name='coursesections', on_delete=models.CASCADE,
                                verbose_name="课程章节")
    name = models.CharField(max_length=128, verbose_name="课时标题")
    section_type = models.SmallIntegerField(default=2, choices=section_type_choices, verbose_name="课时种类")
    section_link = models.CharField(max_length=255, blank=True, null=True, verbose_name="课时链接",
                                    help_text="若是video，填vid,若是文档，填link")
    duration = models.CharField(verbose_name="视频时长", blank=True, null=True, max_length=32)  # 仅在前端展示使用
    lesson_video = models.FileField(upload_to="video", null=True, blank=True, verbose_name="视频")
    pub_date = models.DateTimeField(verbose_name="发布时间", auto_now_add=True)
    free_trail = models.BooleanField(verbose_name="是否可试看", default=False)
    course = models.ForeignKey("Course", related_name="course_lesson", on_delete=models.CASCADE, verbose_name="课程")
    is_show_list = models.BooleanField(verbose_name="是否展示到课程", default=False)

    # lesson = models.IntegerField(verbose_name="第几个课时", default="第一个")

    class Meta:
        db_table = "course_lesson"
        verbose_name = "课程课时"
        verbose_name_plural = "课程课时"

    def __str__(self):
        return "%s-%s" % (self.chapter, self.name)


class Comment(models.Model):
    date = models.DateTimeField(verbose_name="评论时间", auto_now_add=True)
    user = models.ForeignKey(to=UserInfo, related_name='comment_id', on_delete=models.CASCADE, verbose_name="评论用户")
    course = models.ForeignKey('Course', related_name='course_comment', on_delete=models.CASCADE, verbose_name="评论课程")
    text = models.TextField()
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')

    @property
    def username(self):
        return self.user.username

    class Meta:
        db_table = "comment"
        verbose_name = "课程评论"
        verbose_name_plural = "课程评论"

    def __str__(self):
        return "%s-%s" % (self.user.username, self.course.name)
