from celery import shared_task
from datetime import timedelta
from django.core.mail import send_mail
from django.utils import timezone
from config import settings
from lms.models import Course
from users.models import CustomUser


@shared_task
def send_course_update_email(user_id, course_id):
    '''Рассылка писем пользователям об обновлении материалов курса'''

    try:
        user = CustomUser.objects.get(id=user_id)
        course = Course.objects.get(id=course_id)
    except (CustomUser.DoesNotExist, Course.DoesNotExist):
        return

    if timezone.now() - course.updated_at >= timedelta(hours=4):  # minutes=1, hours=4
        # Отправляем уведомление пользователю
        subject = f'Обновление курса: {course.name}'
        message = f'Курс "{course.name}" был обновлён. Проверьте новые материалы!'
        from_email = settings.EMAIL_HOST_USER
        send_mail(subject, message, from_email, [user.email])
    else:
        # Курс обновлялся менее 4 часов назад — не шлём письмо
        return


@shared_task
def deactivate_inactive_users():
    '''Деактивирует неактивных пользователей'''

    one_month_ago = timezone.now() - timedelta(days=30)

    # Фильтруем активных пользователей, не заходивших больше месяца
    inactive_users = CustomUser.objects.filter(is_active=True, last_login__lt=one_month_ago)

    # Обновляем поле is_active
    count = inactive_users.update(is_active=False)

    return f"Deactivated {count} users."
