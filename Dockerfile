# Указываем базовый образ
FROM python:3.13

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файлы с зависимостями
COPY pyproject.toml poetry.lock ./

# Устанавливаем Poetry и зависимости
RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-root

# Копируем остальные файлы проекта в контейнер
COPY . .

RUN mkdir -p /app/media /app/staticfiles && chmod -R 755 /app

# Открываем порт 8000 для взаимодействия с приложением
EXPOSE 8000

# Определяем команду для запуска приложения
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# в DjangoProject
# CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
