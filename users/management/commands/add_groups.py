from django.contrib.auth.models import Group
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = "Create new groups"

    def handle(self, *args, **options):
        Group.objects.all().delete()
        # Создаем новую группу для модераторов
        moderator = Group.objects.create(name="moderator")
        moderator.save()