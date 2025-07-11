from lms.models import Course, Lesson, Subscription
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from lms.validators import validate_url


class SubscriptionSerializer(ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"


class LessonSerializer(ModelSerializer):
    video_url = serializers.URLField(
        required=False,
        allow_null=True,
        validators=[validate_url],
    )

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    subscriptions = SubscriptionSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = "__all__"

    def get_lesson_count(self, obj):
        return obj.lessons.all().count()
