from django.contrib.auth.models import Group
from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):
    help = "add users in group"

    def handle(self, *args, **options):
        moderator = Group.objects.get(name="moderator")
        users_id = input(
            'Введите id пользователей через запятую, которых вы хотите добавить в группу "модераторы":'
        )
        users_id = users_id.split(",")

        for id in users_id:
            try:
                user = User.objects.get(id=id)
                user.groups.add(moderator)
            except Exception as e:
                print(f"Не удалось добавить пользователя с id:{id} в группу ({e})")
                continue
        print("Операция завершена")
