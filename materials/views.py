from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Course, Lesson, Subscriptions
from .paginators import CustomPagination
from .permissions import IsModerator, IsOwner, IsNotModerator
from .serializers import CourseSerializer, LessonSerializer
from rest_framework import viewsets, generics, status


# Create your views here.
class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination

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
    def post(self, request, pk):
        user = request.user
        course_item = Course.objects.get(pk=pk)
        try:
            subs_item = Subscriptions.objects.get(user=user, course=course_item)
        except Subscriptions.DoesNotExist:
            sub = Subscriptions.objects.create(user=user, course=course_item)
            sub.save()
            return Response({'message': 'подписка подключена'}, status=status.HTTP_201_CREATED)
        else:
            subs_item.delete()
            return Response({'message' : 'подписка отключена'}, status=status.HTTP_201_CREATED)


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
        serializer.save(owner=self.request.user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, (IsOwner | IsModerator))


class LessonUpdateAPIView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, (IsModerator | IsOwner))


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsNotModerator, IsOwner)
