from django.contrib import admin
from lms.models import Course, Lesson, Subscription


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'owner', 'updated_at')
    search_fields = ('name',)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'course_id', 'course', 'owner', 'video_url')
    list_filter = ('course',)
    search_fields = ('name',)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'course')
    list_filter = ('course', 'user')
