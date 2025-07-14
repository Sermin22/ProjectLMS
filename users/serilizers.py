from rest_framework import serializers
from users.models import Payments, CustomUser


class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = "__all__"


class CreatePaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = ["date", "paid_course", "paid_lesson", "amount", "session_id", "link"]


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"


class PublicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        # доступные поля публичного профиля
        fields = ["id", "username", "email", "phone_number", "avatar", "city"]
