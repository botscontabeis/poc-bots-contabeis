from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Create a superuser if none exist.

    Example:
        python manage.py createsuperuser_if_none_exists \
            --username=admin --password=admin --email=admin@email.com"""

    def add_arguments(self, parser):
        parser.add_argument("--username", required=True)
        parser.add_argument("--password", required=True)
        parser.add_argument("--email", default="admin@email.com")

    def handle(self, *args, **options):
        User = get_user_model()
        if User.objects.exists():
            return

        username = options["username"]
        password = options["password"]
        email = options["email"]

        User.objects.create_superuser(
            username=username,
            password=password,
            email=email,
        )

        self.stdout.write(f'Superuser "{username}" was created')
