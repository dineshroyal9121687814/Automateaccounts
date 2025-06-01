from django.contrib import admin
from .models import ReceiptFile, Receipt


@admin.register(ReceiptFile)
class ReceiptFileAdmin(admin.ModelAdmin):
    list_display = ['file_name', 'is_valid', 'is_processed', 'created_at']
    list_filter = ['is_valid', 'is_processed', 'created_at']
    search_fields = ['file_name', 'file_path']
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 25
    ordering = ['-created_at']
    
    fieldsets = (
        ('File Information', {
            'fields': ('file_name', 'file_path')
        }),
        ('Validation Status', {
            'fields': ('is_valid', 'invalid_reason', 'is_processed')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ['merchant_name', 'total_amount', 'purchased_at', 'created_at']
    list_filter = ['purchased_at', 'created_at']
    search_fields = ['merchant_name']
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 25
    ordering = ['-created_at']
    date_hierarchy = 'purchased_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('file_path', 'purchased_at', 'merchant_name', 'total_amount')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


# Customize admin site headers
admin.site.site_header = "Receipt Processor Administration"
admin.site.site_title = "Receipt Processor Admin"
admin.site.index_title = "Welcome to Receipt Processor Administration"