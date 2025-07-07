from rest_framework import generics
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from users.models import Payments, CustomUser
from users.permissions import IsOwner
from users.serilizers import PaymentsSerializer, CustomUserSerializer, PublicUserSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter


class PaymentsListAPIView(generics.ListAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ('date',)
    filterset_fields = ('paid_course', 'paid_lesson', 'payment_method')


class CustomUserCreateAPIView(CreateAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    # permission_classes = [AllowAny]  # если в settings.py настройка IsAuthenticated

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(user.password)
        user.save()


class CustomUserListAPIView(ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = PublicUserSerializer
    permission_classes = [IsAuthenticated]


class CustomUserRetrieveAPIView(RetrieveAPIView):
    queryset = CustomUser.objects.all()
    # serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        # Получаем объект пользователя
        obj = self.get_object()
        # Получаем текущего аутентифицированного пользователя
        user = self.request.user
        # Безопасно получаем email текущего пользователя и запрашиваемого объекта
        user_email = getattr(user, 'email', None)
        obj_email = getattr(obj, 'email', None)
        # Проверяем, совпадает ли email запрашиваемого объекта с текущим пользователем
        if obj_email == user_email:
            # Если объекты совпадают, используем полный сериализатор
            return CustomUserSerializer
        else:
            # Иначе используем ограниченный сериализатор
            return PublicUserSerializer


class CustomUserUpdateAPIView(UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated, IsOwner]


class CustomUserDestroyAPIView(DestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated, IsOwner]
