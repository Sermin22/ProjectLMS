from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=250, verbose_name="Курс", help_text="Введите название курса")
    preview_picture = models.ImageField(
        upload_to="lms/course_preview_picture/",
        verbose_name="Превью (картинка)",
        help_text="Добавьте картинку",
        blank=True,
        null=True,
    )
    description = models.TextField(
        verbose_name="Описание курса",
        help_text="Укажите описание курса",
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    name = models.CharField(max_length=250, verbose_name="Урок", help_text="Введите название урока")
    description = models.TextField(
        verbose_name="Описание урока",
        help_text="Укажите описание урока",
        blank=True,
        null=True,
    )
    course = models.ForeignKey(
        to="Course",
        on_delete=models.SET_NULL,
        verbose_name="Курс",
        help_text="Укажите курс",
        blank=True,
        null=True,
        related_name="lessons",
    )
    preview_picture = models.ImageField(
        upload_to="lms/lesson_preview_picture/",
        verbose_name="Превью (картинка)",
        help_text="Добавьте картинку",
        blank=True,
        null=True,
    )
    video_url = models.URLField(
        verbose_name="Ссылка на видео",
        blank=True,
        null=True,
        help_text="Добавьте ссылку на видео",
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
