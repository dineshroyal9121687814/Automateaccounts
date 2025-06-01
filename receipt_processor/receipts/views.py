import os
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.conf import settings
from django.db import transaction
from django.db.models import Sum
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import ReceiptFile, Receipt
from .serializers import ReceiptFileSerializer, ReceiptSerializer
from .services import ReceiptProcessor


@api_view(['POST'])
def upload_receipt(request):
    """Upload a receipt file"""
    if 'file' not in request.FILES:
        return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    file = request.FILES['file']
    if not file.name.lower().endswith('.pdf'):
        return Response({'error': 'Only PDF files allowed'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Save file to receipts_data directory
    file_path = os.path.join(settings.RECEIPTS_DATA_DIR, file.name)
    os.makedirs(settings.RECEIPTS_DATA_DIR, exist_ok=True)
    
    with open(file_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    
    # Create or update database record
    receipt_file, created = ReceiptFile.objects.get_or_create(
        file_name=file.name,
        defaults={'file_path': file_path}
    )
    
    if not created:
        receipt_file.file_path = file_path
        receipt_file.save()
    
    serializer = ReceiptFileSerializer(receipt_file)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def validate_receipt(request):
    """Validate a receipt file"""
    file_id = request.data.get('file_id')
    if not file_id:
        return Response({'error': 'file_id required'}, status=status.HTTP_400_BAD_REQUEST)
    
    receipt_file = get_object_or_404(ReceiptFile, id=file_id)
    
    is_valid, reason = ReceiptProcessor.validate_pdf(receipt_file.file_path)
    
    receipt_file.is_valid = is_valid
    receipt_file.invalid_reason = reason if not is_valid else None
    receipt_file.save()
    
    serializer = ReceiptFileSerializer(receipt_file)
    return Response(serializer.data)


@api_view(['POST'])
def process_receipt(request):
    """Process a receipt file and extract details"""
    file_id = request.data.get('file_id')
    if not file_id:
        return Response({'error': 'file_id required'}, status=status.HTTP_400_BAD_REQUEST)
    
    receipt_file = get_object_or_404(ReceiptFile, id=file_id)
    
    if not receipt_file.is_valid:
        return Response({'error': 'File is not valid'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        with transaction.atomic():
            # Extract text and details
            text = ReceiptProcessor.extract_text_from_pdf(receipt_file.file_path)
            details = ReceiptProcessor.extract_receipt_details(text)
            
            # Create or update receipt record
            receipt, created = Receipt.objects.get_or_create(
                receipt_file=receipt_file,
                defaults={
                    'merchant_name': details.get('merchant_name', ''),
                    'total_amount': details.get('total_amount'),
                    'purchased_at': details.get('purchased_at'),
                    'file_path': receipt_file.file_path,
                }
            )
            
            if not created:
                # Update existing receipt
                receipt.merchant_name = details.get('merchant_name', '')
                receipt.total_amount = details.get('total_amount')
                receipt.purchased_at = details.get('purchased_at')
                receipt.file_path = receipt_file.file_path
                receipt.save()
            
            receipt_file.is_processed = True
            receipt_file.save()
    
    except Exception as e:
        return Response({
            'error': f'Processing failed: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    serializer = ReceiptSerializer(receipt)
    return Response(serializer.data)


@api_view(['GET'])
def list_receipts(request):
    """List all receipts"""
    queryset = Receipt.objects.all().order_by('-created_at')
    serializer = ReceiptSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_receipt(request, receipt_id):
    """Get a specific receipt with full details"""
    receipt = get_object_or_404(Receipt, id=receipt_id)
    serializer = ReceiptSerializer(receipt)
    return Response(serializer.data)


@api_view(['DELETE'])
def delete_receipt(request, receipt_id):
    """Delete a specific receipt"""
    receipt = get_object_or_404(Receipt, id=receipt_id)
    receipt.delete()
    return Response({'message': 'Receipt deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def auto_scan_and_process(request):
    """Auto scan receipts_data directory and process all PDFs"""
    try:
        pdf_files = ReceiptProcessor.scan_receipts_directory()
        processed_count = 0
        errors = []
        
        for file_path in pdf_files:
            try:
                file_name = os.path.basename(file_path)
                
                # Create or get receipt file record
                receipt_file, created = ReceiptFile.objects.get_or_create(
                    file_name=file_name,
                    defaults={'file_path': file_path}
                )
                
                if not created:
                    receipt_file.file_path = file_path
                    receipt_file.save()
                
                # Validate
                is_valid, reason = ReceiptProcessor.validate_pdf(file_path)
                receipt_file.is_valid = is_valid
                receipt_file.invalid_reason = reason if not is_valid else None
                receipt_file.save()
                
                # Process if valid
                if is_valid:
                    with transaction.atomic():
                        text = ReceiptProcessor.extract_text_from_pdf(file_path)
                        details = ReceiptProcessor.extract_receipt_details(text)
                        
                        receipt, created = Receipt.objects.get_or_create(
                            receipt_file=receipt_file,
                            defaults={
                                'merchant_name': details.get('merchant_name', ''),
                                'total_amount': details.get('total_amount'),
                                'purchased_at': details.get('purchased_at'),
                                'file_path': file_path,
                            }
                        )
                        
                        if not created:
                            receipt.merchant_name = details.get('merchant_name', '')
                            receipt.total_amount = details.get('total_amount')
                            receipt.purchased_at = details.get('purchased_at')
                            receipt.file_path = file_path
                            receipt.save()
                        
                        receipt_file.is_processed = True
                        receipt_file.save()
                        processed_count += 1
                        
            except Exception as e:
                errors.append(f"Error processing {file_name}: {str(e)}")
        
        response_data = {
            'message': f'Scanned {len(pdf_files)} files, processed {processed_count} receipts',
            'processed_count': processed_count,
            'total_files': len(pdf_files)
        }
        
        if errors:
            response_data['errors'] = errors
        
        return Response(response_data)
        
    except Exception as e:
        return Response({
            'error': f'Auto scan failed: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def receipt_statistics(request):
    """Get receipt statistics"""
    total_receipts = Receipt.objects.count()
    total_amount = Receipt.objects.aggregate(
        total=Sum('total_amount')
    )['total'] or 0
    
    return Response({
        'total_receipts': total_receipts,
        'total_amount': total_amount,
    })


def dashboard(request):
    """Web dashboard view"""
    receipts = Receipt.objects.all().order_by('-created_at')[:20]
    receipt_files = ReceiptFile.objects.all().order_by('-created_at')[:20]
    
    # Statistics
    total_receipts = Receipt.objects.count()
    total_amount = Receipt.objects.aggregate(
        total=Sum('total_amount')
    )['total'] or 0
    
    valid_files = ReceiptFile.objects.filter(is_valid=True).count()
    processed_files = ReceiptFile.objects.filter(is_processed=True).count()
    
    context = {
        'receipts': receipts,
        'receipt_files': receipt_files,
        'total_receipts': total_receipts,
        'total_amount': total_amount,
        'valid_files': valid_files,
        'processed_files': processed_files,
    }
    return render(request, 'dashboard.html', context)