from django.db import models
from django.contrib.auth.models import User
from transactions.models import Category
from django.conf import settings

class Budget(models.Model):
    name = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    month = models.IntegerField()
    year = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'month', 'year', 'category']
        ordering = ['-year', '-month']

    def __str__(self):
        category_name = self.category.name if self.category else "Overall"
        return f"{self.name} - {category_name} ({self.month}/{self.year})"