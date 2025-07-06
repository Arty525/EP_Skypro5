from django.core.management.base import BaseCommand
from django.core.management import call_command
from users.models import User


class Command(BaseCommand):
    help = "Adds users to database"

    def handle(self, *args, **options):
        User.objects.all().delete()
        call_command("loaddata", "user_fixture.json")
        self.stdout.write(self.style.SUCCESS("Successfully added users"))
