from django.core.management.base import BaseCommand
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db import transaction
from transactions.models import Category, Transaction
from decimal import Decimal
import random
from datetime import date, timedelta

User = get_user_model()

class Command(BaseCommand):
    help = 'Create sample transactions for testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing transactions before seeding',
        )
        parser.add_argument(
            '--user',
            type=str,
            default='testuser',
            help='Username to create transactions for (default: testuser)',
        )
        parser.add_argument(
            '--count',
            type=int,
            default=50,
            help='Number of transactions to create (default: 50)',
        )

    def handle(self, *args, **options):
        try:
            user = User.objects.get(username=options['user'])
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'User "{options["user"]}" does not exist. Please create users first.')
            )
            return

        # Check if categories exist
        categories = Category.objects.filter(user=user)
        if not categories.exists():
            self.stdout.write(
                self.style.ERROR('No categories found. Please seed categories first.')
            )
            return

        if options['clear']:
            self.stdout.write('Clearing existing transactions...')
            Transaction.objects.filter(user=user).delete()

        income_categories = categories.filter(type='income')
        expense_categories = categories.filter(type='expense')

        # Sample transaction data
        income_transactions = [
            {'title': 'Monthly Salary', 'amount_range': (3000, 5000), 'descriptions': ['Regular monthly salary payment', 'Salary deposit']},
            {'title': 'Freelance Project', 'amount_range': (500, 2000), 'descriptions': ['Web development project', 'Design work', 'Consulting fee']},
            {'title': 'Investment Dividend', 'amount_range': (100, 800), 'descriptions': ['Stock dividend payment', 'Mutual fund returns']},
            {'title': 'Side Business Income', 'amount_range': (200, 1500), 'descriptions': ['Online store sales', 'Service income']},
            {'title': 'Bonus Payment', 'amount_range': (500, 3000), 'descriptions': ['Performance bonus', 'Year-end bonus']},
            {'title': 'Gift Money', 'amount_range': (50, 500), 'descriptions': ['Birthday gift', 'Holiday money']},
        ]

        expense_transactions = [
            {'title': 'Grocery Shopping', 'amount_range': (50, 200), 'descriptions': ['Weekly groceries', 'Supermarket shopping', 'Fresh produce']},
            {'title': 'Gas Station', 'amount_range': (30, 80), 'descriptions': ['Fuel for car', 'Gas fill-up']},
            {'title': 'Movie Night', 'amount_range': (15, 50), 'descriptions': ['Cinema tickets', 'Movie streaming subscription']},
            {'title': 'Electric Bill', 'amount_range': (80, 150), 'descriptions': ['Monthly electricity bill', 'Utility payment']},
            {'title': 'Doctor Visit', 'amount_range': (100, 300), 'descriptions': ['Medical consultation', 'Health checkup']},
            {'title': 'Rent Payment', 'amount_range': (800, 2000), 'descriptions': ['Monthly rent', 'Housing payment']},
            {'title': 'Restaurant Dinner', 'amount_range': (25, 100), 'descriptions': ['Dinner out', 'Restaurant meal', 'Date night']},
            {'title': 'Online Shopping', 'amount_range': (20, 200), 'descriptions': ['Amazon purchase', 'Online order', 'Clothing shopping']},
            {'title': 'Course Fee', 'amount_range': (100, 500), 'descriptions': ['Online course', 'Training program', 'Educational material']},
            {'title': 'Car Insurance', 'amount_range': (100, 300), 'descriptions': ['Monthly insurance premium', 'Auto insurance']},
            {'title': 'Netflix Subscription', 'amount_range': (10, 20), 'descriptions': ['Streaming service', 'Monthly subscription']},
            {'title': 'Weekend Trip', 'amount_range': (200, 800), 'descriptions': ['Travel expenses', 'Hotel booking', 'Vacation cost']},
            {'title': 'Haircut', 'amount_range': (20, 60), 'descriptions': ['Salon visit', 'Hair styling']},
            {'title': 'Home Repair', 'amount_range': (50, 500), 'descriptions': ['Plumbing fix', 'Maintenance work', 'Home improvement']},
            {'title': 'Coffee Shop', 'amount_range': (5, 15), 'descriptions': ['Morning coffee', 'Cafe visit']},
        ]

        transactions_created = 0
        
        with transaction.atomic():
            # Generate transactions for the last 6 months
            end_date = date.today()
            start_date = end_date - timedelta(days=180)
            
            for _ in range(options['count']):
                # Random date within the range
                random_days = random.randint(0, (end_date - start_date).days)
                transaction_date = start_date + timedelta(days=random_days)
                
                # Decide if it's income or expense (20% income, 80% expense)
                is_income = random.random() < 0.2
                
                if is_income and income_categories.exists():
                    transaction_type = 'income'
                    category = random.choice(income_categories)
                    transaction_template = random.choice(income_transactions)
                else:
                    transaction_type = 'expense'
                    category = random.choice(expense_categories)
                    
                    # Match category with appropriate transaction template
                    if category.name == 'Groceries':
                        transaction_template = {'title': 'Grocery Shopping', 'amount_range': (50, 200), 'descriptions': ['Weekly groceries', 'Supermarket shopping']}
                    elif category.name == 'Transportation':
                        transaction_template = {'title': 'Gas Station', 'amount_range': (30, 80), 'descriptions': ['Fuel for car', 'Public transport']}
                    elif category.name == 'Entertainment':
                        transaction_template = {'title': 'Movie Night', 'amount_range': (15, 50), 'descriptions': ['Cinema tickets', 'Concert tickets']}
                    elif category.name == 'Utilities':
                        transaction_template = {'title': 'Electric Bill', 'amount_range': (80, 150), 'descriptions': ['Monthly electricity bill', 'Water bill']}
                    elif category.name == 'Healthcare':
                        transaction_template = {'title': 'Doctor Visit', 'amount_range': (100, 300), 'descriptions': ['Medical consultation', 'Pharmacy']}
                    elif category.name == 'Rent/Mortgage':
                        transaction_template = {'title': 'Rent Payment', 'amount_range': (800, 2000), 'descriptions': ['Monthly rent', 'Mortgage payment']}
                    elif category.name == 'Dining Out':
                        transaction_template = {'title': 'Restaurant Dinner', 'amount_range': (25, 100), 'descriptions': ['Dinner out', 'Lunch meeting']}
                    elif category.name == 'Shopping':
                        transaction_template = {'title': 'Online Shopping', 'amount_range': (20, 200), 'descriptions': ['Amazon purchase', 'Clothing shopping']}
                    else:
                        transaction_template = random.choice(expense_transactions)
                
                # Generate amount within range
                min_amount, max_amount = transaction_template['amount_range']
                amount = Decimal(str(round(random.uniform(min_amount, max_amount), 2)))
                
                # Create transaction
                Transaction.objects.create(
                    title=transaction_template['title'],
                    description=random.choice(transaction_template['descriptions']),
                    amount=amount,
                    type=transaction_type,
                    category=category,
                    user=user,
                    date=transaction_date
                )
                
                transactions_created += 1

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {transactions_created} transactions for user: {user.username}!')
        )
        
        # Show summary
        income_count = Transaction.objects.filter(user=user, type='income').count()
        expense_count = Transaction.objects.filter(user=user, type='expense').count()
        total_income = sum(t.amount for t in Transaction.objects.filter(user=user, type='income'))
        total_expenses = sum(t.amount for t in Transaction.objects.filter(user=user, type='expense'))
        
        self.stdout.write(f'Income transactions: {income_count} (Total: ${total_income})')
        self.stdout.write(f'Expense transactions: {expense_count} (Total: ${total_expenses})')
        self.stdout.write(f'Balance: ${total_income - total_expenses}')