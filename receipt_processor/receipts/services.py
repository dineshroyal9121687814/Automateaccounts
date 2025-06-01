import os
import re
import PyPDF2
import pytesseract
from pdf2image import convert_from_path
from decimal import Decimal
from datetime import datetime
from django.conf import settings


class ReceiptProcessor:
    
    @staticmethod
    def validate_pdf(file_path):
        """Validate if file is a valid PDF"""
        try:
            with open(file_path, 'rb') as file:
                PyPDF2.PdfReader(file)
            return True, None
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def extract_text_from_pdf(file_path):
        """Extract text from PDF using OCR"""
        try:
            # First try to extract text directly from PDF
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() or ""
            
            # If no text found, use OCR
            if not text.strip():
                images = convert_from_path(file_path)
                text = ""
                for image in images:
                    text += pytesseract.image_to_string(image)
            
            return text
        except Exception as e:
            print(f"Error extracting text: {e}")
            return ""
    
    @staticmethod
    def extract_receipt_details(text):
        """Extract merchant name, amount, and date from text"""
        details = {
            'merchant_name': '',
            'total_amount': None,
            'purchased_at': None
        }
        
        # Extract total amount
        amount_patterns = [
            r'total[:\s]*\$?(\d+\.?\d*)',
            r'\$(\d+\.\d{2})',
            r'amount[:\s]*\$?(\d+\.?\d*)',
            r'(\d+\.\d{2})'
        ]
        
        for pattern in amount_patterns:
            matches = re.findall(pattern, text.lower())
            if matches:
                try:
                    details['total_amount'] = Decimal(matches[-1])
                    break
                except:
                    continue
        
        # Extract merchant name (first line)
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        if lines:
            details['merchant_name'] = lines[0][:100]
        
        # Extract date
        date_patterns = [
            r'(\d{1,2}/\d{1,2}/\d{4})',
            r'(\d{4}-\d{2}-\d{2})',
            r'(\d{1,2}-\d{1,2}-\d{4})'
        ]
        
        for pattern in date_patterns:
            matches = re.findall(pattern, text)
            if matches:
                try:
                    date_str = matches[0]
                    if '/' in date_str:
                        details['purchased_at'] = datetime.strptime(date_str, '%m/%d/%Y')
                    elif '-' in date_str and len(date_str.split('-')[0]) == 4:
                        details['purchased_at'] = datetime.strptime(date_str, '%Y-%m-%d')
                    else:
                        details['purchased_at'] = datetime.strptime(date_str, '%m-%d-%Y')
                    break
                except:
                    continue
        
        return details

    @staticmethod
    def scan_receipts_directory():
        """Scan receipts_data directory for PDF files"""
        receipts_dir = settings.RECEIPTS_DATA_DIR
        pdf_files = []
        
        for root, dirs, files in os.walk(receipts_dir):
            for file in files:
                if file.lower().endswith('.pdf'):
                    pdf_files.append(os.path.join(root, file))
        
        return pdf_files