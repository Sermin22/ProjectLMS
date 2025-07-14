import re
from rest_framework import serializers


def validate_url(value):
    """
    Проверяет, что ссылка ведет только на youtube.com или youtu.be, используя re.
    """
    if not value:
        return  # пустое значение допустимо

    # Пример шаблона, который ищет youtube.com или youtu.be в домене
    pattern = re.compile(r'^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.be)\/.*', re.IGNORECASE)

    if not pattern.match(value):
        raise serializers.ValidationError(
            'Можно прикреплять только ссылки на youtube.com или youtu.be.'
        )
