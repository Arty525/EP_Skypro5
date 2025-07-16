from celery import shared_task
from django.utils import timezone
from datetime import timedelta
import logging
import os
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent

tasks_logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler()
console_formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(name)s - %(message)s - %(pathname)s:%(lineno)d")
console_handler.setFormatter(console_formatter)
file_handler = logging.FileHandler(os.path.join(ROOT_DIR,"logs", "users","tasks.log"), "w")
file_formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(name)s - %(message)s - %(pathname)s:%(lineno)d")
file_handler.setFormatter(file_formatter)
tasks_logger.addHandler(file_handler)
tasks_logger.setLevel(logging.INFO)

@shared_task
def check_last_login(user):
    print('CCCCCCCCC')
    if user.last_login is not None:
        if timezone.now() - user.last_login > timedelta(month=1):
            user.is_active = False
            tasks_logger.info(f'User {user} blocked by time')
            print('AAAAAAAAAAAAAAAAAAA')
            user.save()
    else:
        print('BBBBBBBBBBBBBBBB')
        tasks_logger.info(f'User {user} last_login is None')