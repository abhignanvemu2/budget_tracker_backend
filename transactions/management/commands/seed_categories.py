from django.core.management.base import BaseCommand
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db import transaction
from transactions.models import Category

User = get_user_model()
class Command(BaseCommand):
    help = 'Create sample categories for testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing categories before seeding',
        )
        parser.add_argument(
            '--user',
            type=str,
            default='testuser',
            help='Username to create categories for (default: testuser)',
        )

    def handle(self, *args, **options):
        try:
            user = User.objects.get(username=options['user'])
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'User "{options["user"]}" does not exist. Please create users first.')
            )
            return

        if options['clear']:
            self.stdout.write('Clearing existing categories...')
            Category.objects.filter(user=user).delete()

        # Income categories
        income_categories = [
            {'name': 'Salary', 'type': 'income', 'color': '#10B981'},
            {'name': 'Freelance', 'type': 'income', 'color': '#059669'},
            {'name': 'Investment Returns', 'type': 'income', 'color': '#047857'},
            {'name': 'Side Business', 'type': 'income', 'color': '#065F46'},
            {'name': 'Bonus', 'type': 'income', 'color': '#064E3B'},
            {'name': 'Gift Money', 'type': 'income', 'color': '#022C22'},
        ]

        # Expense categories
        expense_categories = [
            {'name': 'Groceries', 'type': 'expense', 'color': '#EF4444'},
            {'name': 'Transportation', 'type': 'expense', 'color': '#DC2626'},
            {'name': 'Entertainment', 'type': 'expense', 'color': '#B91C1C'},
            {'name': 'Utilities', 'type': 'expense', 'color': '#991B1B'},
            {'name': 'Healthcare', 'type': 'expense', 'color': '#7F1D1D'},
            {'name': 'Rent/Mortgage', 'type': 'expense', 'color': '#450A0A'},
            {'name': 'Dining Out', 'type': 'expense', 'color': '#F97316'},
            {'name': 'Shopping', 'type': 'expense', 'color': '#EA580C'},
            {'name': 'Education', 'type': 'expense', 'color': '#3B82F6'},
            {'name': 'Insurance', 'type': 'expense', 'color': '#2563EB'},
            {'name': 'Subscriptions', 'type': 'expense', 'color': '#8B5CF6'},
            {'name': 'Travel', 'type': 'expense', 'color': '#7C3AED'},
            {'name': 'Personal Care', 'type': 'expense', 'color': '#EC4899'},
            {'name': 'Home Maintenance', 'type': 'expense', 'color': '#F59E0B'},
            {'name': 'Miscellaneous', 'type': 'expense', 'color': '#6B7280'},
        ]

        all_categories = income_categories + expense_categories

        with transaction.atomic():
            for category_data in all_categories:
                category, created = Category.objects.get_or_create(
                    name=category_data['name'],
                    user=user,
                    defaults={
                        'type': category_data['type'],
                        'color': category_data['color']
                    }
                )
                
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(f'Created {category.type} category: {category.name}')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f'Category already exists: {category.name}')
                    )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully seeded categories for user: {user.username}!')
        )
        self.stdout.write(f'Created {len(income_categories)} income categories')
        self.stdout.write(f'Created {len(expense_categories)} expense categories')