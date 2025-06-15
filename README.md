# Personal Budget Tracker - Backend

Django REST Framework backend for the Personal Budget Tracker application.

## 🏗 Architecture

```
backend/
├── budget_tracker/          # Main Django project
│   ├── settings.py         # Django settings
│   ├── urls.py            # URL routing
│   └── wsgi.py            # WSGI configuration
├── accounts/              # User authentication
│   ├── models.py          # User model extensions
│   ├── views.py           # Auth views
│   ├── serializers.py     # Auth serializers
│   └── urls.py            # Auth URLs
├── transactions/          # Transaction management
│   ├── models.py          # Transaction & Category models
│   ├── views.py           # Transaction views
│   ├── serializers.py     # Transaction serializers
│   └── urls.py            # Transaction URLs
├── budgets/              # Budget management
│   ├── models.py          # Budget models
│   ├── views.py           # Budget views
│   ├── serializers.py     # Budget serializers
│   └── urls.py            # Budget URLs
└── manage.py             # Django management script
```

## 🔌 API Endpoints

### Authentication Endpoints
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `GET /api/auth/profile/` - Get user profile

### Transaction Endpoints
- `GET /api/transactions/` - List transactions with filtering
- `POST /api/transactions/` - Create new transaction
- `GET /api/transactions/{id}/` - Get transaction details
- `PUT /api/transactions/{id}/` - Update transaction
- `DELETE /api/transactions/{id}/` - Delete transaction
- `GET /api/transactions/summary/` - Get financial summary

### Category Endpoints
- `GET /api/transactions/categories/` - List categories
- `POST /api/transactions/categories/` - Create category
- `GET /api/transactions/categories/{id}/` - Get category details
- `PUT /api/transactions/categories/{id}/` - Update category
- `DELETE /api/transactions/categories/{id}/` - Delete category

### Budget Endpoints
- `GET /api/budgets/` - List budgets with filtering
- `POST /api/budgets/` - Create budget
- `GET /api/budgets/{id}/` - Get budget details
- `PUT /api/budgets/{id}/` - Update budget
- `DELETE /api/budgets/{id}/` - Delete budget
- `GET /api/budgets/analysis/` - Get budget analysis

## 🔧 Setup Instructions

### 1. Environment Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Configuration

Create `.env` file from `.env.example`:

```bash
cp .env.example .env
```

Configure your environment variables:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=postgresql://user:password@host:port/database
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:8000
```

### 3. Database Setup

```bash
# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Seed database with sample data
python seed_all.py
```

### 4. Start Development Server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`

## 🌱 Database Seeding

### Quick Seeding (Recommended)

```bash
python seed_all.py
```
### Manual Seeding

```bash
# Create users
python manage.py seed_users --clear

# Create categories
python manage.py seed_categories --clear --user=testuser

# Create transactions
python manage.py seed_transactions --clear --user=testuser --count=75

# Create budgets
python manage.py seed_budgets --clear --user=testuser
```

### Test Credentials

After seeding:
- **Username**: `testuser`
- **Password**: `testpass123`

## 🔐 Authentication

The API uses JWT (JSON Web Tokens) for authentication:

### Login Process
1. POST credentials to `/api/auth/login/`
2. Receive `access` and `refresh` tokens
3. Include `Authorization: Bearer <access_token>` in subsequent requests
4. Use refresh token to get new access token when expired

### Token Configuration
- Access token lifetime: 24 hours
- Refresh token lifetime: 7 days
- Automatic token rotation enabled

## 📊 API Features

### Filtering & Pagination
- **Transactions**: Filter by type, category, date range, amount
- **Categories**: Filter by type (income/expense)
- **Budgets**: Filter by month, year, category
- **Pagination**: 20 items per page by default

### Search Functionality
- **Transactions**: Search by title and description
- **Categories**: Search by name

### Sorting
- **Transactions**: Sort by date, amount, created_at
- **Categories**: Sort by name, created_at
- **Budgets**: Sort by year, month

## 🛡 Security Features

### Authentication & Authorization
- JWT token-based authentication
- User-specific data isolation
- Permission-based access control

### Data Protection
- SQL injection prevention via Django ORM
- XSS protection through serializer validation
- CORS configuration for frontend access
- Environment variable management

### Input Validation
- Comprehensive serializer validation
- Custom validation rules for financial data
- Error handling with detailed messages

## 🧪 Testing

### Run Tests
```bash
python manage.py test
```

### Test Coverage
```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html 
```

### API Testing
Use Django REST Framework's browsable API at `http://localhost:8000/api/`

## 📈 Performance Optimization

### Database Optimization
- Proper indexing on frequently queried fields
- Select related for foreign key relationships
- Pagination to limit query results

### Caching (Optional)
- Redis integration ready
- Cache configuration in settings
- API response caching for expensive queries

### Query Optimization
- Efficient database queries
- Bulk operations for data seeding
- Optimized serializers

## 🚀 Deployment

### Production Settings
1. Set `DEBUG=False`
2. Configure production database
3. Set secure `SECRET_KEY`
4. Configure `ALLOWED_HOSTS`
5. Set up static file serving
6. Configure HTTPS settings

### Environment Variables
```env
SECRET_KEY=production-secret-key
DEBUG=False
DATABASE_URL=postgresql://user:pass@host:port/db
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
CORS_ALLOWED_ORIGINS=https://yourdomain.com
```

### Deployment Platforms
- **Railway**: Easy PostgreSQL integration
- **onRender** : simple backend deployment
- **Vercel** : frontend deployment

## 🔍 Monitoring & Logging

### Logging Configuration
- Configurable log levels
- File and console logging
- Error tracking and debugging

### Health Checks
- Database connectivity checks
- API endpoint monitoring
- Performance metrics
