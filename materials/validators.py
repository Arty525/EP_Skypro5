from rest_framework.serializers import ValidationError


class VideoUrlValidator:
    def __init__(self, field):
        self.url = field

    def __call__(self, fields):
        print(fields['video_url'])
        if not 'youtube.com' in fields['video_url']:
            raise ValidationError('Запрещены ссылки на сторонние ресурсы кроме youtube.com')