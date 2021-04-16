from rest_framework.serializers import ModelSerializer
from course.models import CourseCategory, Course, Teacher


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