from django.urls import path
from . import views

urlpatterns = [
    path('', views.BudgetListCreateView.as_view(), name='budget-list'),
    path('<int:pk>/', views.BudgetDetailView.as_view(), name='budget-detail'),
    path('analysis/', views.budget_analysis, name='budget-analysis'),
]