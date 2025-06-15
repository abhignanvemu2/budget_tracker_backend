from django.contrib import admin
from .models import Budget

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ['name', 'amount', 'category', 'user', 'month', 'year']
    list_filter = ['month', 'year', 'category']
    search_fields = ['name', 'user__username']