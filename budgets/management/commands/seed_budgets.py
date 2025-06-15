from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction
from budgets.models import Budget
from transactions.models import Category
from decimal import Decimal
import random
from datetime import date

User = get_user_model()

class Command(BaseCommand):
    help = 'Create sample budgets for testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing budgets before seeding',
        )
        parser.add_argument(
            '--user',
            type=str,
            default='testuser',
            help='Username to create budgets for (default: testuser)',
        )

    def handle(self, *args, **options):
        try:
            user = User.objects.get(username=options['user'])
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'User "{options["user"]}" does not exist. Please create users first.')
            )
            return

        expense_categories = Category.objects.filter(user=user, type='expense')
        if not expense_categories.exists():
            self.stdout.write(
                self.style.ERROR('No expense categories found. Please seed categories first.')
            )
            return

        if options['clear']:
            self.stdout.write('Clearing existing budgets...')
            Budget.objects.filter(user=user).delete()

        current_date = date.today()
        current_month = current_date.month
        current_year = current_date.year

        budget_templates = [
            {'name': 'Groceries Budget', 'category': 'Groceries', 'amount_range': (400, 600)},
            {'name': 'Transportation Budget', 'category': 'Transportation', 'amount_range': (200, 400)},
            {'name': 'Entertainment Budget', 'category': 'Entertainment', 'amount_range': (150, 300)},
            {'name': 'Utilities Budget', 'category': 'Utilities', 'amount_range': (200, 350)},
            {'name': 'Healthcare Budget', 'category': 'Healthcare', 'amount_range': (300, 500)},
            {'name': 'Dining Out Budget', 'category': 'Dining Out', 'amount_range': (200, 400)},
            {'name': 'Shopping Budget', 'category': 'Shopping', 'amount_range': (300, 600)},
            {'name': 'Personal Care Budget', 'category': 'Personal Care', 'amount_range': (100, 200)},
            {'name': 'Subscriptions Budget', 'category': 'Subscriptions', 'amount_range': (50, 150)},
            {'name': 'Travel Budget', 'category': 'Travel', 'amount_range': (500, 1000)},
        ]

        budgets_created = 0

        with transaction.atomic():
            for month_offset in [0, 1]:
                target_month = current_month + month_offset
                target_year = current_year
                
                if target_month > 12:
                    target_month = target_month - 12
                    target_year += 1

                overall_budget_amount = Decimal(str(random.randint(3000, 5000)))
                Budget.objects.create(
                    name=f'Overall Budget - {target_month}/{target_year}',
                    amount=overall_budget_amount,
                    category=None,
                    user=user,
                    month=target_month,
                    year=target_year
                )
                budgets_created += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created overall budget: ${overall_budget_amount} for {target_month}/{target_year}')
                )

                available_categories = list(expense_categories)
                random.shuffle(available_categories)
                
                num_budgets = random.randint(5, min(8, len(available_categories)))
                
                for i in range(num_budgets):
                    category = available_categories[i]
                    
                    template = None
                    for temp in budget_templates:
                        if temp['category'] == category.name:
                            template = temp
                            break
                    
                    if not template:
                        template = {
                            'name': f'{category.name} Budget',
                            'category': category.name,
                            'amount_range': (100, 500)
                        }
                    
                    min_amount, max_amount = template['amount_range']
                    amount = Decimal(str(random.randint(min_amount, max_amount)))
                    
                    existing_budget = Budget.objects.filter(
                        user=user,
                        category=category,
                        month=target_month,
                        year=target_year
                    ).first()
                    
                    if not existing_budget:
                        Budget.objects.create(
                            name=template['name'],
                            amount=amount,
                            category=category,
                            user=user,
                            month=target_month,
                            year=target_year
                        )
                        budgets_created += 1
                        self.stdout.write(
                            self.style.SUCCESS(f'Created budget: {template["name"]} - ${amount} for {target_month}/{target_year}')
                        )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {budgets_created} budgets for user: {user.username}!')
        )
        
        current_month_budgets = Budget.objects.filter(
            user=user, 
            month=current_month, 
            year=current_year
        ).count()
        
        total_budget_amount = sum(
            b.amount for b in Budget.objects.filter(
                user=user, 
                month=current_month, 
                year=current_year
            )
        )
        
        self.stdout.write(f'Current month budgets: {current_month_budgets}')
        self.stdout.write(f'Total budget amount for current month: ${total_budget_amount}')