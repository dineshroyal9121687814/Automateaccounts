from django.urls import path
from . import views

urlpatterns = [
    # Web interface
    path('', views.dashboard, name='dashboard'),
    
    # File management
    path('upload/', views.upload_receipt, name='upload'),
    path('validate/', views.validate_receipt, name='validate'),
    path('process/', views.process_receipt, name='process'),
    path('auto-scan/', views.auto_scan_and_process, name='auto-scan'),
    
    # Receipt management
    path('receipts/', views.list_receipts, name='receipts'),
    path('receipts/<int:receipt_id>/', views.get_receipt, name='receipt-detail'),
    path('receipts/<int:receipt_id>/delete/', views.delete_receipt, name='receipt-delete'),
    
    # Statistics
    path('statistics/', views.receipt_statistics, name='statistics'),
]