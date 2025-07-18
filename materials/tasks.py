from celery import shared_task
from django.core.mail import send_mail
from config import settings
from materials.models import Subscriptions, Course
import logging
import os
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent

tasks_logger = logging.getLogger(__name__)
file_handler = logging.FileHandler(
    os.path.join(ROOT_DIR, "logs", "materials", "tasks.log"), "w"
)
file_formatter = logging.Formatter(
    "[%(asctime)s] %(levelname)s - %(name)s - %(message)s - %(pathname)s:%(lineno)d"
)
file_handler.setFormatter(file_formatter)
tasks_logger.addHandler(file_handler)
tasks_logger.setLevel(logging.DEBUG)


@shared_task
def send_course_update_mail(course_pk):
    course = Course.objects.get(pk=course_pk)
    subject = f'Курс "{course.title} обновлен."'
    message = (
        f'Курс "{course.title}" обновлен. '
        f"Вы получили это сообщение, потому что подписаны на обновления этого курса."
    )
    subs = Subscriptions.objects.filter(course=course)
    recipient_list = []
    for recipient in subs:
        recipient_list.append(recipient.user.email)
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        recipient_list,
        fail_silently=False,
    )
    return "Сообщение отправлено"
