from rest_framework import status
from rest_framework.test import APITestCase
from users.models import CustomUser
from django.urls import reverse
from lms.models import Lesson, Course


class LessonTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(email="test@mail.ru")
        self.course = Course.objects.create(
            name="Курс для теста",
            description="Описание курса для теста"
        )
        self.lesson = Lesson.objects.create(
            name="Урок для теста",
            description="Описание урока для теста",
            course=self.course,
            owner=self.user,
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse("lms:lessons_retrieve", args=[self.lesson.pk])
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get("name"), "Урок для теста"
        )

    def test_lesson_create(self):
        url = reverse("lms:lessons_create")
        data = {
            "name": "Урок для теста create"
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            Lesson.objects.all().count(), 2
        )
        data = response.json()
        self.assertEqual(
            data.get("name"), "Урок для теста create"
        )

    def test_lesson_update(self):
        url = reverse("lms:lessons_update", args=[self.lesson.pk])
        data = {
            "name": "Урок для теста update"
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get("name"), "Урок для теста update"
        )

    def test_lesson_delete(self):
        url = reverse("lms:lessons_delete", args=[self.lesson.pk])
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Lesson.objects.all().count(), 0
        )

    def test_lesson_list(self):
        url = reverse("lms:lessons_list")
        response = self.client.get(url)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "video_url": None,
                    "name": "Урок для теста",
                    "description": "Описание урока для теста",
                    "preview_picture": None,
                    "course": self.course.pk,
                    "owner": self.user.pk
                }
            ]
        }
        self.assertEqual(
            data, result
        )


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(email="test@mail.ru")
        self.course = Course.objects.create(
            name="Курс для теста",
            description="Описание курса для теста",
            owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_course_subscription(self):
        url = reverse("lms:subscription_toggle")
        data = {
            "course_id": self.course.pk
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        data = response.json()
        result = {"message": "Подписка добавлена"}
        self.assertEqual(
            data, result
        )

    def test_course_subscription_deleted(self):
        url = reverse("lms:subscription_toggle")
        data = {"course_id": self.course.pk}
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        data_deleted = {"course_id": self.course.pk}
        response = self.client.post(url, data_deleted)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        data_deleted = response.json()
        result = {"message": "Подписка удалена"}
        self.assertEqual(
            data_deleted, result
        )
