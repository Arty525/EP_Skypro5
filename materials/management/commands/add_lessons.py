from django.core.management.base import BaseCommand
from django.core.management import call_command
from materials.models import Lesson

class Command(BaseCommand):
    help = 'Adds lessons to database'

    def handle(self, *args, **options):
        Lesson.objects.all().delete()
        call_command('loaddata', 'lesson_fixture.json')
        self.stdout.write(self.style.SUCCESS('Successfully added lessons'))