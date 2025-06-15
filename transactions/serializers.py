from rest_framework import serializers
from .models import Category, Transaction
from helpers import CATEGEORY_ERRORS

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'type', 'color', 'created_at']
        read_only_fields = ['created_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class TransactionSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_color = serializers.CharField(source='category.color', read_only=True)

    class Meta:
        model = Transaction
        fields = [
            'id', 'title', 'description', 'amount', 'type', 
            'category', 'category_name', 'category_color', 
            'date', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    def validate_category(self, value):
        if value.user != self.context['request'].user:
            raise serializers.ValidationError(CATEGEORY_ERRORS.YOU_CAN_ONLY_USE_YOUR_OWN_CATEGORIES)
        return value