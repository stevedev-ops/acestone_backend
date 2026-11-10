from django.db import models
from django.conf import settings
from apps.inventory.models import JewelleryItem

class SaleTransaction(models.Model):
    class PaymentMethod(models.TextChoices):
        MPESA = 'M-Pesa', 'M-Pesa'
        CASH = 'Cash', 'Cash'
        CARD = 'Card', 'Card'
        BANK_TRANSFER = 'Bank Transfer', 'Bank Transfer'
        SPLIT = 'Split', 'Split Payment'

    class PaymentStatus(models.TextChoices):
        COMPLETED = 'Completed', 'Completed'
        PARTIAL = 'Partial', 'Partial Deposit'
        REFUNDED = 'Refunded', 'Refunded'

    receipt_number = models.CharField(max_length=50, unique=True, db_index=True)
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sales', on_delete=models.PROTECT)
    employee_name = models.CharField(max_length=150)
    
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    discount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    total_gross_profit = models.DecimalField(max_digits=12, decimal_places=2)

    payment_method = models.CharField(max_length=30, choices=PaymentMethod.choices)
    payment_status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.COMPLETED)
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2)
    balance_due = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    customer_name = models.CharField(max_length=150, blank=True)
    customer_phone = models.CharField(max_length=50, blank=True)
    customer_notes = models.TextField(blank=True)

    approved_by = models.CharField(max_length=150, blank=True)
    is_returned = models.BooleanField(default=False)
    return_reason = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.receipt_number} - KSh {self.total_amount}"

class SaleItem(models.Model):
    transaction = models.ForeignKey(SaleTransaction, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(JewelleryItem, related_name='sale_records', on_delete=models.PROTECT)
    product_code = models.CharField(max_length=50)
    product_name = models.CharField(max_length=255)
    
    # Historical financial snapshot at the time of sale
    original_buying_cost = models.DecimalField(max_digits=12, decimal_places=2)
    suggested_price = models.DecimalField(max_digits=12, decimal_places=2)
    negotiated_selling_price = models.DecimalField(max_digits=12, decimal_places=2)
    gross_profit = models.DecimalField(max_digits=12, decimal_places=2)

    approved_by = models.CharField(max_length=150, blank=True)
    approval_notes = models.TextField(blank=True)

class ApprovalRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        APPROVED = 'APPROVED', 'Approved'
        REJECTED = 'REJECTED', 'Rejected'

    product = models.ForeignKey(JewelleryItem, on_delete=models.CASCADE)
    product_code = models.CharField(max_length=50)
    product_name = models.CharField(max_length=255)
    suggested_price = models.DecimalField(max_digits=12, decimal_places=2)
    min_selling_price = models.DecimalField(max_digits=12, decimal_places=2)
    proposed_price = models.DecimalField(max_digits=12, decimal_places=2)
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    employee_name = models.CharField(max_length=150)
    reason = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    approved_by = models.CharField(max_length=150, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class NotebookDailySale(models.Model):
    class ItemType(models.TextChoices):
        JEWELLERY = 'JEWELLERY', 'Jewellery Piece'
        SERVICE = 'SERVICE', 'Service (0 Stock)'
        UNLINKED = 'UNLINKED', 'Unlinked Entry'

    item_description = models.CharField(max_length=255)
    item_type = models.CharField(max_length=20, choices=ItemType.choices, default=ItemType.JEWELLERY)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=30)
    payment_status = models.CharField(max_length=20, default='Completed')
    
    product = models.ForeignKey(JewelleryItem, null=True, blank=True, on_delete=models.SET_NULL)
    product_code = models.CharField(max_length=50, blank=True)
    compartment_code = models.CharField(max_length=50, blank=True)

    recorded_by = models.CharField(max_length=150)
    customer_name = models.CharField(max_length=150, blank=True)
    customer_phone = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True)
    reconciled = models.BooleanField(default=False)
    reconciled_with_product_id = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.item_description} - KSh {self.amount} ({self.item_type})"

class DailyRegisterClosing(models.Model):
    class Status(models.TextChoices):
        BALANCED = 'BALANCED', 'Balanced'
        DISCREPANCY = 'DISCREPANCY', 'Discrepancy'
        PENDING = 'PENDING', 'Pending Review'

    closing_date = models.DateField(auto_now_add=True)
    total_sales = models.DecimalField(max_digits=12, decimal_places=2)
    total_cash_expected = models.DecimalField(max_digits=12, decimal_places=2)
    total_cash_counted = models.DecimalField(max_digits=12, decimal_places=2)
    cash_difference = models.DecimalField(max_digits=12, decimal_places=2)
    total_mpesa_paybill = models.DecimalField(max_digits=12, decimal_places=2)
    total_card_bank = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    services_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_items_count = models.PositiveIntegerField(default=0)
    
    # Banknote counts
    k1000_count = models.PositiveIntegerField(default=0)
    k500_count = models.PositiveIntegerField(default=0)
    k200_count = models.PositiveIntegerField(default=0)
    k100_count = models.PositiveIntegerField(default=0)
    k50_count = models.PositiveIntegerField(default=0)

    signed_off_by = models.CharField(max_length=150)
    signed_off_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.BALANCED)
    closing_notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-signed_off_at']

    def __str__(self):
        return f"Closing {self.closing_date} by {self.signed_off_by} - {self.status}"


