from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction

User = get_user_model()

class Command(BaseCommand):
    help = 'Create sample users for testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing users before seeding',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing users...')
            User.objects.filter(is_superuser=False).delete()

        users_data = [
            {
                'username': 'testuser',
                'email': 'testuser@example.com',
                'password': 'testpass123',
                'first_name': 'Test',
                'last_name': 'User'
            },
            {
                'username': 'johndoe',
                'email': 'john.doe@example.com',
                'password': 'password123',
                'first_name': 'John',
                'last_name': 'Doe'
            },
            {
                'username': 'janedoe',
                'email': 'jane.doe@example.com',
                'password': 'password123',
                'first_name': 'Jane',
                'last_name': 'Doe'
            },
            {
                'username': 'demouser',
                'email': 'demo@example.com',
                'password': 'demo123',
                'first_name': 'Demo',
                'last_name': 'User'
            }
        ]

        with transaction.atomic():
            for user_data in users_data:
                user, created = User.objects.get_or_create(
                    username=user_data['username'],
                    defaults={
                        'email': user_data['email'],
                        'first_name': user_data['first_name'],
                        'last_name': user_data['last_name']
                    }
                )
                
                if created:
                    user.set_password(user_data['password'])
                    user.save()
                    self.stdout.write(
                        self.style.SUCCESS(f'Created user: {user.username}')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f'User already exists: {user.username}')
                    )

        self.stdout.write(
            self.style.SUCCESS('Successfully seeded users!')
        )
        self.stdout.write('\nTest Credentials:')
        self.stdout.write('Username: testuser | Password: testpass123')
        self.stdout.write('Username: johndoe | Password: password123')
        self.stdout.write('Username: janedoe | Password: password123')
        self.stdout.write('Username: demouser | Password: demo123')