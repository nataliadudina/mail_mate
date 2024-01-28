from main.services import schedule
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    To run: python manage.py run_scheduler <your_email>@yandex.ru
    """

    help = "Runs APScheduler."

    def add_arguments(self, parser):
        # Adds an argument to pass the user's email
        parser.add_argument('user_email', nargs='+', type=str)

    def handle(self, *args, **options):
        # Gets user's email from command line arguments
        user_email = options['user_email'][0]
        schedule(user_email)
