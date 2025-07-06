from django.core.management.base import BaseCommand
from django.core.management import call_command
from materials.models import Course


class Command(BaseCommand):
    help = "Adds courses to database"

    def handle(self, *args, **options):
        Course.objects.all().delete()
        call_command("loaddata", "course_fixture.json")
        self.stdout.write(self.style.SUCCESS("Successfully added courses"))
