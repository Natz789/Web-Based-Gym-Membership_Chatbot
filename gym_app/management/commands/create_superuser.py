from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from decouple import config

User = get_user_model()


class Command(BaseCommand):
    help = 'Create a superuser from environment variables or default credentials'

    def handle(self, *args, **options):
        # Get credentials from environment variables with defaults
        username = config('SUPERUSER_USERNAME', default='admin')
        email = config('SUPERUSER_EMAIL', default='admin@gym.com')
        password = config('SUPERUSER_PASSWORD', default='admin')

        # Check if superuser already exists
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.SUCCESS(f'Superuser "{username}" already exists')
            )
            return

        # Create superuser
        try:
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
                first_name='Admin',
                last_name='User',
                role='admin'
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully created superuser "{username}" with password "{password}"'
                )
            )
            self.stdout.write(
                self.style.WARNING(
                    f'⚠️  Default credentials are being used! '
                    f'Username: {username} | Password: {password}'
                )
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating superuser: {str(e)}')
            )
