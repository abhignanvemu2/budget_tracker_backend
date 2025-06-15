from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum
from datetime import date
from .models import Budget
from .serializers import BudgetSerializer
from transactions.models import Transaction

class BudgetListCreateView(generics.ListCreateAPIView):
    serializer_class = BudgetSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['month', 'year', 'category']

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)

class BudgetDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BudgetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def budget_analysis(request):
    user = request.user
    
    today = date.today()
    month = int(request.GET.get('month', today.month))
    year = int(request.GET.get('year', today.year))
    
    budgets = Budget.objects.filter(user=user, month=month, year=year)
    
    start_date = date(year, month, 1)
    if month == 12:
        end_date = date(year + 1, 1, 1)
    else:
        end_date = date(year, month + 1, 1)
    
    expenses = Transaction.objects.filter(
        user=user,
        type='expense',
        date__gte=start_date,
        date__lt=end_date
    )
    
    total_budgeted = budgets.aggregate(total=Sum('amount'))['total'] or 0
    total_spent = expenses.aggregate(total=Sum('amount'))['total'] or 0
    
    budget_comparison = []
    for budget in budgets:
        category_expenses = expenses.filter(category=budget.category) if budget.category else expenses
        category_spent = category_expenses.aggregate(total=Sum('amount'))['total'] or 0
        
        budget_comparison.append({
            'budget_id': budget.id,
            'budget_name': budget.name,
            'category': budget.category.name if budget.category else 'Overall',
            'budgeted_amount': float(budget.amount),
            'spent_amount': float(category_spent),
            'remaining_amount': float(budget.amount) - float(category_spent),
            'percentage_used': round((float(category_spent) / float(budget.amount)) * 100, 2) if budget.amount > 0 else 0,
            'over_budget': float(category_spent) > float(budget.amount)
        })
    
    return Response({
        'period': {
            'month': month,
            'year': year
        },
        'summary': {
            'total_budgeted': float(total_budgeted),
            'total_spent': float(total_spent),
            'total_remaining': float(total_budgeted) - float(total_spent),
            'overall_percentage': round((float(total_spent) / float(total_budgeted)) * 100, 2) if total_budgeted > 0 else 0
        },
        'budget_comparison': budget_comparison
    })