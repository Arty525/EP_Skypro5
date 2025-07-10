from rest_framework.serializers import ValidationError


class VideoUrlValidator:
    def __init__(self, field):
        self.url = field

    def __call__(self, fields):
        if fields.get("video_url"):
            if "youtube.com" not in fields["video_url"]:
                raise ValidationError(
                    "Запрещены ссылки на сторонние ресурсы кроме youtube.com"
                )
