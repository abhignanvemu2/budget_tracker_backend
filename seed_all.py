#!/usr/bin/env python
"""
Master seeder script to populate the database with sample data.
Run this script to seed all data at once.
"""
import os
import sys
import django
from django.core.management import call_command

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'budget_tracker.settings')
django.setup()

def main():
    print("🌱 Starting database seeding process...")
    print("=" * 50)
    
    try:
        # Step 1: Seed users
        print("\n1️⃣ Seeding users...")
        call_command('seed_users', '--clear')
        
        # Step 2: Seed categories for testuser
        print("\n2️⃣ Seeding categories...")
        call_command('seed_categories', '--clear', '--user=testuser')
        
        # Step 3: Seed transactions for testuser
        print("\n3️⃣ Seeding transactions...")
        call_command('seed_transactions', '--clear', '--user=testuser', '--count=75')
        
        # Step 4: Seed budgets for testuser
        print("\n4️⃣ Seeding budgets...")
        call_command('seed_budgets', '--clear', '--user=testuser')
        
        print("\n" + "=" * 50)
        print("✅ Database seeding completed successfully!")
        print("\n🔑 Test Credentials:")
        print("Username: testuser")
        print("Password: testpass123")
        print("\n📊 Sample data includes:")
        print("- 4 test users")
        print("- 21 categories (6 income + 15 expense)")
        print("- 75 transactions (last 6 months)")
        print("- Budget plans for current and next month")
        print("\n🚀 You can now start the development server and test the application!")
        
    except Exception as e:
        print(f"\n❌ Error during seeding: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()