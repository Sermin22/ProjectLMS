from lms.models import Course, Lesson
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer


class CourseSerializer(ModelSerializer):
    lesson_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    def get_lesson_count(self, obj):
        lesson_count = obj.lessons.all().count()
        if lesson_count:
            return lesson_count
        return None


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
