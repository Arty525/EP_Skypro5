from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase, APIClient

from materials.models import Lesson, Course, Subscriptions
from users.models import User


# Create your tests here.


class LessonsAPIViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@testmail.ru", password="testpass123"
        )
        self.second_user = User.objects.create_user(
            email="test2@testmail.ru", password="testpass123"
        )
        Course.objects.create(
            id=1,
            title="Course 1",
            description="Course description 1",
            preview="course_prev_1",
        )
        self.client = APIClient()
        self.lesson = Lesson.objects.create(
            title="Test lesson1",
            description="Test desc1",
            video_url="https://youtube.com/watch?v=1",
            course=Course.objects.get(id=1),
            owner=User.objects.first(),
        )

    def test_delete_lesson(self):
        lesson = Lesson.objects.create(
            title="Test lesson2",
            description="Test desc2",
            video_url="https://youtube.com/watch?v=1",
            course=Course.objects.get(id=1),
            owner=User.objects.first(),
        )
        url = reverse("materials:lesson_delete", kwargs={"pk": lesson.pk})
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_lesson_owner(self):
        lesson = Lesson.objects.create(
            title="Test lesson2",
            description="Test desc2",
            video_url="https://youtube.com/watch?v=1",
            course=Course.objects.get(id=1),
            owner=User.objects.first(),
        )
        url = reverse("materials:lesson_delete", kwargs={"pk": lesson.pk})
        self.client.force_authenticate(user=self.second_user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_lesson_unauthenticated(self):
        lesson = Lesson.objects.create(
            title="Test lesson2",
            description="Test desc2",
            video_url="https://youtube.com/watch?v=1",
            course=Course.objects.get(id=1),
            owner=User.objects.first(),
        )
        url = reverse("materials:lesson_delete", kwargs={"pk": lesson.pk})
        self.client.force_authenticate(user=None)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_list(self):
        url = reverse("materials:lesson_list")
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_get_list_unauthenticated(self):
        url = reverse("materials:lesson_list")
        self.client.force_authenticate(user=None)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_lesson_create(self):
        url = reverse("materials:lesson_create")
        data = {
            "title": "Test lesson create",
            "description": "Test desc",
            "video_url": "https://youtube.com/watch?v=test",
            "course": 1,
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "Test lesson create")
        self.assertEqual(Lesson.objects.all().count(), 2)

        data = {
            "title": "Test lesson create",
            "description": "Test desc",
            "video_url": "https://vk.com/watch?v=test",
            "course": 1,
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        self.assertRaises(ValidationError)

    def test_lesson_create_unauthenticated(self):
        url = reverse("materials:lesson_create")
        data = {
            "title": "Test lesson",
            "description": "Test desc",
            "video_url": "https://youtube.com/watch?v=test",
            "course": 1,
        }
        self.client.force_authenticate(user=None)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_lesson_partial_update(self):
        url = reverse("materials:lesson_update", kwargs={"pk": self.lesson.pk})
        data = {"title": "Partial updated lesson"}
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Partial updated lesson")

    def test_lesson_partial_update_unauthenticated(self):
        url = reverse("materials:lesson_update", kwargs={"pk": self.lesson.pk})
        data = {"title": "Partial updated lesson"}
        self.client.force_authenticate(user=None)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_lesson_partial_update_owner(self):
        url = reverse("materials:lesson_update", kwargs={"pk": self.lesson.pk})
        data = {"title": "Partial updated lesson"}
        self.client.force_authenticate(user=self.second_user)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_full_update(self):
        url = reverse("materials:lesson_update", kwargs={"pk": self.lesson.pk})
        data = {
            "title": "Full updated lesson",
            "description": "Updated lesson",
            "video_url": "https://youtube.com/watch?v=updated",
            "course": 1,
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Full updated lesson")

    def test_lesson_full_update_unauthenticated(self):
        url = reverse("materials:lesson_update", kwargs={"pk": self.lesson.pk})
        data = {
            "title": "Full updated lesson",
            "description": "Updated lesson",
            "video_url": "https://youtube.com/watch?v=updated",
            "course": 1,
        }
        self.client.force_authenticate(user=None)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_lesson_full_update_owner(self):
        url = reverse("materials:lesson_update", kwargs={"pk": self.lesson.pk})
        data = {
            "title": "Full updated lesson",
            "description": "Updated lesson",
            "video_url": "https://youtube.com/watch?v=updated",
            "course": 1,
        }
        self.client.force_authenticate(user=self.second_user)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class SubscriptionAPIViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="test@testmail.ru", password="1234")
        self.course = Course.objects.create(
            id=1, title="Test course", description="Test course"
        )
        self.client = APIClient()
        self.url = reverse("materials:course_subscribe", kwargs={"pk": self.course.pk})

    def test_subscription(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post(self.url, {"pk": self.course.pk})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "подписка подключена")
        self.assertEqual(Subscriptions.objects.all().count(), 1)

        response = self.client.post(self.url, {"pk": self.course.pk})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "подписка отключена")
        self.assertEqual(Subscriptions.objects.all().count(), 0)

    def test_subscription_create_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.post(self.url, {"pk": self.course.pk})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
