from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from lms.models import Course, Lesson
from lms.serilizers import CourseSerializer, LessonSerializer
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView

from users.permissions import IsNotModer, IsModer, IsOwner


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    # Пользователь, создавший курс становится владельцем этого курса
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

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
