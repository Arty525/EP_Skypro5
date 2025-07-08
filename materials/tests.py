from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, force_authenticate, APIClient

from materials.models import Lesson, Course
from users.models import User


# Create your tests here.

class LessonsListAPIViewTestCase(APITestCase):
    def setUp(self):
        Course.objects.create(id=111, title='Course 1', description='Course description 1', preview='course_prev_1')

        Lesson.objects.create(title='Test lesson1', description='Test desc1', preview='preview1.jpg', video_url='https://youtube.com/watch?v=1', course=Course.objects.get(id=111))
        Lesson.objects.create(title='Test lesson2', description='Test desc2', preview='preview2.jpg', video_url='https://youtube.com/watch?v=2', course=Course.objects.get(id=111))
        Lesson.objects.create(title='Test lesson3', description='Test desc3', preview='preview3.jpg', video_url='https://youtube.com/watch?v=3', course=Course.objects.get(id=111))
        Lesson.objects.create(title='Test lesson4', description='Test desc4', preview='preview4.jpg', video_url='https://youtube.com/watch?v=4', course=Course.objects.get(id=111))
        self.url = reverse('materials:lesson_list')
        self.client = APIClient()
        self.user = User.objects.create_user(email='test@testmail.ru', password='testpass123')

    def test_get(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 4)