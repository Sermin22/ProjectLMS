from rest_framework import generics
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from users.models import Payments, CustomUser
from users.permissions import IsOwner
from users.serilizers import PaymentsSerializer, CustomUserSerializer, PublicUserSerializer, CreatePaymentsSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from users.services import create_product_stripe, create_price_stripe, create_session_stripe, payment_status
from rest_framework.response import Response


class PaymentsListAPIView(generics.ListAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ('date',)
    filterset_fields = ('paid_course', 'paid_lesson', 'payment_method')


class PaymentsCreateAPIView(CreateAPIView):
    serializer_class = CreatePaymentsSerializer
    queryset = Payments.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        product = create_product_stripe()
        price = create_price_stripe(payment.amount, product)
        session_id, payment_link = create_session_stripe(price)
        payment.session_id = session_id
        payment.link = payment_link
        payment.save()


class PaymentsStatusAPIView(APIView):
    """Получает статус сессии оплаты."""

    def get(self, request, session_id=None):
        if not session_id:
            return Response({"detail": "Session ID is required."}, status=400)

        try:
            # Получаем статус сессии через функцию payment_status
            session_data = payment_status(session_id)

            # Возвращаем успешный ответ с данными сессии
            return Response({
                "session_id": session_id,
                "status": session_data.status,
                "payment_intent_id": session_data.payment_intent,
                "customer": session_data.customer,
                "customer_email": session_data.customer_email,
                "amount_total": session_data.amount_total / 100,
                "currency": session_data.currency,
                "payment_status": session_data.payment_status
            })
        except Exception as e:
            return Response({"detail": f"Ошибка при извлечении данных оплаты: {str(e)}"}, status=500)


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
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """Определяем сериализатор при выводе данных. Владельцу все поля"""

        if self.request.user.id == int(self.kwargs['pk']):
            return CustomUserSerializer

        else:
            return PublicUserSerializer

        # # Получаем объект пользователя
        # obj = self.get_object()
        # # Получаем текущего аутентифицированного пользователя
        # user = self.request.user
        # # Безопасно получаем email текущего пользователя и запрашиваемого объекта
        # user_email = getattr(user, 'email', None)
        # obj_email = getattr(obj, 'email', None)
        # # Проверяем, совпадает ли email запрашиваемого объекта с текущим пользователем
        # if obj_email == user_email:
        #     # Если объекты совпадают, используем полный сериализатор
        #     return CustomUserSerializer
        # else:
        #     # Иначе используем ограниченный сериализатор
        #     return PublicUserSerializer


class CustomUserUpdateAPIView(UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated, IsOwner]


class CustomUserDestroyAPIView(DestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated, IsOwner]
