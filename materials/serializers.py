from rest_framework import serializers
from materials.models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):

    lessons_count = serializers.SerializerMethodField()

    class LessonShortSerializer(serializers.ModelSerializer):
        """Сериализатор для краткого отображения уроков внутри курса."""

        class Meta:
            model = Lesson
            fields = ("id", "title")

    lessons = LessonShortSerializer(many=True, read_only=True, source="lesson_set")

    def get_lessons_count(self, instance):
        return instance.lesson_set.count()


    class Meta:
        model = Course
        fields = "__all__"


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
