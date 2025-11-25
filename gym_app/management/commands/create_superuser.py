from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from decouple import config

User = get_user_model()


class Command(BaseCommand):
    help = 'Create a superuser from environment variables'

    def handle(self, *args, **options):
        # Get credentials from environment variables
        username = config('SUPERUSER_USERNAME', default=None)
        email = config('SUPERUSER_EMAIL', default=None)
        password = config('SUPERUSER_PASSWORD', default=None)

        if not username or not email or not password:
            self.stdout.write(
                self.style.WARNING(
                    'Skipping superuser creation. Set SUPERUSER_USERNAME, '
                    'SUPERUSER_EMAIL, and SUPERUSER_PASSWORD environment variables.'
                )
            )
            return

        # Check if superuser already exists
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.SUCCESS(f'Superuser "{username}" already exists')
            )
            return

        # Create superuser
        try:
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created superuser "{username}"')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating superuser: {str(e)}')
            )
