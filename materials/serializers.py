from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from materials.models import Course, Lesson, Subscriptions
from materials.validators import VideoUrlValidator


class CourseSerializer(serializers.ModelSerializer):

    lessons_count = serializers.SerializerMethodField()
    lessons = serializers.SerializerMethodField()
    subscription = serializers.SerializerMethodField()

    def get_subscription(self, instance):
        try:
            sub = Subscriptions.objects.get(course=instance)
            return sub.user == self.context["request"].user
        except ObjectDoesNotExist:
            return False

    def get_lessons_count(self, instance):
        return instance.lesson_set.count()

    def get_lessons(self, instance):
        lessons = instance.lesson_set.all()
        return LessonSerializer(lessons, many=True).data

    class Meta:
        model = Course
        fields = "__all__"


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [VideoUrlValidator(field="video_url")]
