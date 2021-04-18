from rest_framework.serializers import ModelSerializer

from course.models import CourseCategory, Course, Teacher, Comment


class CourseCategoryModelSerializer(ModelSerializer):
    """课程分类序列化器"""

    class Meta:
        model = CourseCategory
        fields = ["id", "name"]


class TeacherModelSerializer(ModelSerializer):
    """讲师的序列化器"""

    class Meta:
        model = Teacher
        fields = ["id", "name", "title"]


class CourseModelSerializer(ModelSerializer):
    """课程信息序列化器"""

    teacher = TeacherModelSerializer()

    class Meta:
        model = Course
        fields = ["id", "name", "course_img", "students", "pub_lessons", "lessons",
                  "price", 'course_type', 'teacher', 'lesson_list']


class TeacherInfoModelSerializer(ModelSerializer):
    """讲师的序列化器"""

    class Meta:
        model = Teacher
        fields = ['name', 'title', 'role_name', 'signature', 'image', 'brief']


class CourseInfoModelSerializer(ModelSerializer):
    """课程信息序列化器"""

    teacher = TeacherInfoModelSerializer()

    class Meta:
        model = Course
        # fields = ["id", "name", "course_img", "students", "pub_lessons", "lessons", "price", 'course_type', 'teacher', 'lesson_list']
        fields = ['id', 'teacher', 'name', 'course_video', 'type', 'brief', 'level_n', 'students', 'lessons',
                  'pub_lessons', 'price', 'lesson_info']


class CommentModelSerializer(ModelSerializer):
    """评论信息序列化器"""

    class Meta:
        model = Comment
        fields = ['id', 'username', 'user', 'course', 'text', 'date', 'is_delete']

        extra_kwargs = {
            "id": {
                "read_only": True
            },
            "is_delete": {
                "write_only": True
            },
            "date": {
                "read_only": True
            },
            "username": {
                "read_only": True
            },
            "user": {
                "write_only": True
            },
        }
