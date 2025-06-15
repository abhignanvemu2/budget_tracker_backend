from rest_framework import serializers
from .models import Budget
from transactions.models import Transaction, Category
from django.db.models import Sum
from datetime import date
from helpers import CATEGEORY_ERRORS

class BudgetSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    spent_amount = serializers.SerializerMethodField()
    remaining_amount = serializers.SerializerMethodField()
    percentage_used = serializers.SerializerMethodField()

    class Meta:
        model = Budget
        fields = [
            'id', 'name', 'amount', 'category', 'category_name', 
            'month', 'year', 'spent_amount', 'remaining_amount', 
            'percentage_used', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_spent_amount(self, obj):
        start_date = date(obj.year, obj.month, 1)
        if obj.month == 12:
            end_date = date(obj.year + 1, 1, 1)
        else:
            end_date = date(obj.year, obj.month + 1, 1)
        
        spent = Transaction.objects.filter(
            user=obj.user,
            type='expense',
            date__gte=start_date,
            date__lt=end_date
        )
        
        if obj.category:
            spent = spent.filter(category=obj.category)
            
        return float(spent.aggregate(total=Sum('amount'))['total'] or 0)

    def get_remaining_amount(self, obj):
        spent = self.get_spent_amount(obj)
        return float(obj.amount) - spent

    def get_percentage_used(self, obj):
        spent = self.get_spent_amount(obj)
        if obj.amount > 0:
            return round((spent / float(obj.amount)) * 100, 2)
        return 0

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    def validate_category(self, value):
        if value and value.user != self.context['request'].user:
            raise serializers.ValidationError(CATEGEORY_ERRORS.YOU_CAN_ONLY_USE_YOUR_OWN_CATEGORIES)
        return value