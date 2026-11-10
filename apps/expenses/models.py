from django.db import models
from django.conf import settings

class Expense(models.Model):
    class Category(models.TextChoices):
        RENT = 'Rent', 'Rent'
        SALARIES = 'Salaries', 'Salaries'
        ELECTRICITY = 'Electricity', 'Electricity'
        SECURITY = 'Security', 'Security'
        TRANSPORT = 'Transport', 'Transport'
        INSURANCE = 'Insurance', 'Insurance'
        OTHER = 'Other', 'Other'

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=Category.choices)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    description = models.TextField(blank=True)
    recorded_by = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.title} ({self.category}) - KSh {self.amount}"

