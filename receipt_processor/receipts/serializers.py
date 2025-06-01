from rest_framework import serializers
from .models import ReceiptFile, Receipt


class ReceiptFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReceiptFile
        fields = ['id', 'file_name', 'file_path', 'is_valid', 'invalid_reason', 'is_processed', 'created_at', 'updated_at']


class ReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receipt
        fields = ['id', 'receipt_file', 'purchased_at', 'merchant_name', 'total_amount', 'file_path', 'created_at', 'updated_at']