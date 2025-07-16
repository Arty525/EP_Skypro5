from datetime import timezone, datetime, timedelta

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import Payments
from users.serializers import PaymentSerializer
from .models import Course, Lesson, Subscriptions
from .paginators import CustomPagination
from .permissions import IsModerator, IsOwner, IsNotModerator
from .serializers import CourseSerializer, LessonSerializer
from rest_framework import viewsets, generics, status
from .services import create_stripe_price, create_stripe_session
from .tasks import send_course_update_mail
import logging
import os
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent

views_logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler()
console_formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(name)s - %(message)s - %(pathname)s:%(lineno)d")
console_handler.setFormatter(console_formatter)
file_handler = logging.FileHandler(os.path.join(ROOT_DIR,"logs", "materials","views.log"), "w")
file_formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(name)s - %(message)s - %(pathname)s:%(lineno)d")
file_handler.setFormatter(file_formatter)
views_logger.addHandler(file_handler)
views_logger.setLevel(logging.DEBUG)


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination

    def update(self, request, *args, **kwargs):
        views_logger.info(('CourseViewSet.update started'))
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            if timedelta(hours=4) >= datetime.now(timezone.utc) - instance.last_updated:
                send_course_update_mail.delay(instance.pk,)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (~IsModerator,)
        elif self.action in ["update", "partial_update", "retrieve"]:
            self.permission_classes = (IsModerator | IsOwner,)
        elif self.action == "destroy":
            self.permission_classes = (~IsModerator | IsOwner,)
        return super().get_permissions()


class CourseSubscribeAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        user = request.user
        course_item = Course.objects.get(pk=pk)
        try:
            subs_item = Subscriptions.objects.get(user=user, course=course_item)
        except Subscriptions.DoesNotExist:
            sub = Subscriptions.objects.create(user=user, course=course_item)
            sub.save()
            return Response(
                {"message": "подписка подключена"}, status=status.HTTP_201_CREATED
            )
        else:
            subs_item.delete()
            return Response(
                {"message": "подписка отключена"}, status=status.HTTP_201_CREATED
            )


class LessonListAPIView(generics.ListAPIView):
    pagination_class = CustomPagination
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsOwner)


class LessonCreateAPIView(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsNotModerator)

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(owner=self.request.user)
            course = Course.objects.get(pk=self.request.data['course'])
            course.last_updated = datetime.now(timezone.utc)
            if timedelta(hours=4) >= datetime.now(timezone.utc) - course.last_updated:
                course.last_updated = datetime.now(timezone.utc)
            course.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, (IsOwner | IsModerator))


class LessonUpdateAPIView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, (IsModerator | IsOwner))

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            course = Course.objects.get(pk=serializer.data['course'])
            if timedelta(hours=4) <= datetime.now(timezone.utc) - course.last_updated:
                course.last_updated = datetime.now(timezone.utc)
            course.save()
            views_logger.info(f'Урок {serializer.data['title']} обновлен. Курс {course} обновлен.')
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsNotModerator, IsOwner)


class PaymentCreateAPIView(generics.CreateAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentSerializer

    def get_course(self):
        course_id = self.kwargs.get("pk")
        return Course.objects.get(pk=course_id)

    def perform_create(self, serializer, *args, **kwargs):
        course_item = self.get_course()
        payment = serializer.save(user=self.request.user, course=course_item)
        price = create_stripe_price(course_item)
        session_id, payment_link = create_stripe_session(price)
        payment.session_id = session_id
        payment.payment_link = payment_link
        payment.payment_method = "перевод на счет"
        payment.save()
        return Response({"payment_link", payment_link}, status=status.HTTP_201_CREATED)
