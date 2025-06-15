# Database Seeders Documentation

This document explains how to use the database seeders to populate your Personal Budget Tracker application with sample data for testing and demonstration purposes.

## Overview

The seeder system includes management commands to create:
- **Users**: Test user accounts with different credentials
- **Categories**: Income and expense categories with colors
- **Transactions**: Sample financial transactions over the last 6 months
- **Budgets**: Monthly budget plans for expense tracking

## Quick Start

### Option 1: Seed Everything at Once (Recommended)

```bash
cd backend
python seed_all.py
```

This will create all sample data with default settings and provide you with test credentials.

### Option 2: Manual Seeding (Step by Step)

```bash
cd backend

# 1. Create users
python manage.py seed_users --clear

# 2. Create categories for testuser
python manage.py seed_categories --clear --user=testuser

# 3. Create transactions for testuser
python manage.py seed_transactions --clear --user=testuser --count=75

# 4. Create budgets for testuser
python manage.py seed_budgets --clear --user=testuser
```

## Individual Seeder Commands

### 1. User Seeder

Creates test user accounts for the application.

```bash
python manage.py seed_users [--clear]
```

**Options:**
- `--clear`: Remove existing non-superuser accounts before seeding

**Created Users:**
- `testuser` / `testpass123` (Primary test account)
- `johndoe` / `password123`
- `janedoe` / `password123`
- `demouser` / `demo123`

### 2. Category Seeder

Creates income and expense categories with color coding.

```bash
python manage.py seed_categories [--clear] [--user=USERNAME]
```

**Options:**
- `--clear`: Remove existing categories for the user
- `--user=USERNAME`: Specify which user to create categories for (default: testuser)

**Created Categories:**
- **Income (6)**: Salary, Freelance, Investment Returns, Side Business, Bonus, Gift Money
- **Expense (15)**: Groceries, Transportation, Entertainment, Utilities, Healthcare, Rent/Mortgage, Dining Out, Shopping, Education, Insurance, Subscriptions, Travel, Personal Care, Home Maintenance, Miscellaneous

### 3. Transaction Seeder

Creates realistic financial transactions over the past 6 months.

```bash
python manage.py seed_transactions [--clear] [--user=USERNAME] [--count=NUMBER]
```

**Options:**
- `--clear`: Remove existing transactions for the user
- `--user=USERNAME`: Specify which user to create transactions for (default: testuser)
- `--count=NUMBER`: Number of transactions to create (default: 50)

**Transaction Features:**
- Random dates within the last 6 months
- 20% income, 80% expense ratio (realistic distribution)
- Category-appropriate transaction titles and descriptions
- Realistic amount ranges based on category type
- Varied transaction patterns for authentic data

### 4. Budget Seeder

Creates monthly budget plans for current and next month.

```bash
python manage.py seed_budgets [--clear] [--user=USERNAME]
```

**Options:**
- `--clear`: Remove existing budgets for the user
- `--user=USERNAME`: Specify which user to create budgets for (default: testuser)

**Budget Features:**
- Overall monthly budget (no specific category)
- Category-specific budgets for 5-8 random expense categories
- Realistic budget amounts based on category type
- Budgets for both current and next month

## Sample Data Overview

After running the seeders, you'll have:

### Users
- 4 test accounts with different credentials
- Ready-to-use login credentials for testing

### Categories
- 6 income categories with green color scheme
- 15 expense categories with varied color coding
- Proper categorization for financial tracking

### Transactions
- 75+ realistic transactions spanning 6 months
- Balanced mix of income and expenses
- Category-appropriate amounts and descriptions
- Authentic spending patterns

### Budgets
- Overall monthly budgets ($3,000-$5,000)
- Category-specific budgets with realistic limits
- Current and future month planning
- Budget vs. actual comparison data

## Test Credentials

After seeding, use these credentials to test the application:

**Primary Test Account:**
- Username: `testuser`
- Password: `testpass123`

**Additional Accounts:**
- Username: `johndoe` | Password: `password123`
- Username: `janedoe` | Password: `password123`
- Username: `demouser` | Password: `demo123`

## Customization

### Creating Data for Different Users

```bash
# Seed data for a specific user
python manage.py seed_categories --user=johndoe
python manage.py seed_transactions --user=johndoe --count=100
python manage.py seed_budgets --user=johndoe
```

### Adjusting Transaction Volume

```bash
# Create more transactions for richer data
python manage.py seed_transactions --count=150 --user=testuser

# Create fewer transactions for simpler testing
python manage.py seed_transactions --count=25 --user=testuser
```

## Clearing Data

Each seeder supports the `--clear` flag to remove existing data before creating new records:

```bash
# Clear and recreate all data
python manage.py seed_users --clear
python manage.py seed_categories --clear --user=testuser
python manage.py seed_transactions --clear --user=testuser
python manage.py seed_budgets --clear --user=testuser
```

## Troubleshooting

### Common Issues

1. **"User does not exist" error**
   - Run `python manage.py seed_users` first
   - Ensure the username exists before seeding other data

2. **"No categories found" error**
   - Run `python manage.py seed_categories` before seeding transactions or budgets
   - Categories are required for transactions and budgets

3. **Permission errors**
   - Ensure you're in the `backend` directory
   - Check that Django settings are properly configured

### Verification

After seeding, verify the data was created:

```bash
# Check in Django admin or shell
python manage.py shell

# In the shell:
from django.contrib.auth.models import User
from transactions.models import Category, Transaction
from budgets.models import Budget

print(f"Users: {User.objects.count()}")
print(f"Categories: {Category.objects.count()}")
print(f"Transactions: {Transaction.objects.count()}")
print(f"Budgets: {Budget.objects.count()}")
```

## Production Considerations

⚠️ **Important**: These seeders are designed for development and testing only.

- Never run seeders in production environments
- The `--clear` flag will delete existing data
- Test credentials use simple passwords for development convenience
- Sample data is fictional and for demonstration purposes only

## Integration with Frontend

Once seeded, the frontend application will have:
- Immediate access to realistic financial data
- Pre-populated charts and visualizations
- Functional budget tracking and comparisons
- Complete transaction history for testing filters and pagination

The seeded data provides a comprehensive foundation for testing all application features without manual data entry.