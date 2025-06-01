from django.db import models
from django.utils import timezone


class ReceiptFile(models.Model):
    file_name = models.CharField(max_length=255)
    file_path = models.CharField(max_length=500)
    is_valid = models.BooleanField(default=False)
    invalid_reason = models.TextField(blank=True, null=True)
    is_processed = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.file_name

    class Meta:
        db_table = 'receipt_file'


class Receipt(models.Model):
    receipt_file = models.ForeignKey(ReceiptFile, on_delete=models.CASCADE, related_name='receipts')
    purchased_at = models.DateTimeField(null=True, blank=True)
    merchant_name = models.CharField(max_length=255, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    file_path = models.CharField(max_length=500)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.merchant_name} - {self.total_amount}"

    class Meta:
        db_table = 'receipt'