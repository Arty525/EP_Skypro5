from django.core.management.base import BaseCommand
from django.core.management import call_command
from users.models import Payments

class Command(BaseCommand):
    help = 'Adds payments to database'

    def handle(self, *args, **options):
        Payments.objects.all().delete()
        call_command('loaddata', 'payment_fixture.json')
        self.stdout.write(self.style.SUCCESS('Successfully added payments'))