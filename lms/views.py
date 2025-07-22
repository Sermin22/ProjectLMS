from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from lms.models import Course, Lesson, Subscription
from lms.paginators import LmsPagination
from lms.serilizers import CourseSerializer, LessonSerializer
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from django.shortcuts import get_object_or_404
from users.permissions import IsNotModer, IsModer, IsOwner
from lms.tasks import send_course_update_email


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = LmsPagination

    # Пользователь, создавший курс становится владельцем этого курса
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        course = serializer.save()
        subscriptions = Subscription.objects.filter(course=course)
        for sub in subscriptions:
            send_course_update_email.delay(sub.user.id, course.id)

    def get_permissions(self):
        # если создание, право не модератора
        if self.action == "create":
            permission_classes = [IsNotModer]
        # если удаление, то право не модератора и владельца
        elif self.action in ["destroy"]:
            permission_classes = [IsNotModer, IsOwner]
        # если просмотр или обновление, то право модератора или владельца
        elif self.action in ["retrieve", "update", "partial_update"]:
            permission_classes = [IsModer | IsOwner]
        else:
            permission_classes = self.permission_classes  # дефолтные, например IsAuthenticated
        return [permission() for permission in permission_classes]


class LessonCreateAPIView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsNotModer]

    # Пользователь, создавший урок становится владельцем этого урока
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListAPIView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = LmsPagination


class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModer | IsOwner]


class LessonUpdateAPIView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModer | IsOwner]


class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsNotModer, IsOwner]


class SubscriptionToggleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get("course_id")

        if not course_id:
            return Response({"error": "Не передан course_id"}, status=400)

        course = get_object_or_404(Course, id=course_id)

        # Проверяем, есть ли уже подписка
        subs_item = Subscription.objects.filter(user=user, course=course)

        if subs_item.exists():
            subs_item.delete()
            message = "Подписка удалена"
        else:
            Subscription.objects.create(user=user, course=course)
            message = "Подписка добавлена"

        return Response({"message": message})
