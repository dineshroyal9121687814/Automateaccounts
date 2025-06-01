Receipt Processor
A Django-based application for processing receipt PDF files, extracting key details (merchant name, total amount, purchase date), and managing them via a REST API and web dashboard. The application uses SQLite as the database and supports uploading, validating, and processing PDF receipts.
Project Structure

manage.py: Django management script.
receipt_processor/: Django project directory containing settings, URLs, and application code.
receipts/: Application directory with models, views, serializers, and services.
receipts_data/: Directory for storing uploaded PDF receipt files.
db.sqlite3: SQLite database file.
requirements.txt: Python dependencies.
venv/: Virtual environment directory.

Prerequisites

Python 3.8+: Ensure Python is installed (python3 --version).
Tesseract OCR: Required for PDF text extraction via OCR.
Ubuntu: sudo apt-get install tesseract-ocr libtesseract-dev
Windows: Install Tesseract from here and add to PATH.
macOS: brew install tesseract


Poppler: Required for pdf2image to convert PDFs to images.
Ubuntu: sudo apt-get install poppler-utils
Windows: Install Poppler from here and add to PATH.
macOS: brew install poppler



Setup Instructions

Clone the Repository or Navigate to Project Directory
cd ~/ProjectA/automateAccounts/receipt_processor


Set Up Virtual EnvironmentCreate and activate a virtual environment:
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install DependenciesInstall the required Python packages from requirements.txt:
pip install -r requirements.txt

The requirements.txt should contain:
asgiref==3.8.1
Django==4.2.7
django-cors-headers==4.3.1
djangorestframework==3.14.0
packaging==25.0
pdf2image==1.16.3
Pillow==10.1.0
PyPDF2==3.0.1
pytesseract==0.3.10
pytz==2025.2
sqlparse==0.5.3
typing_extensions==4.13.2


Configure Django SettingsEnsure the settings.py file in receipt_processor/ includes:
RECEIPTS_DATA_DIR = os.path.join(BASE_DIR, 'receipts_data')

This specifies the directory for storing uploaded PDF files.

Apply Database MigrationsInitialize the SQLite database:
python manage.py makemigrations
python manage.py migrate


Create Superuser (Optional for Admin Access)To access the Django admin interface:
python manage.py createsuperuser


Run the Development ServerStart the Django server:
python manage.py runserver

The server will run at http://127.0.0.1:8000/.


Running the Application

Web Dashboard: Access the dashboard at http://127.0.0.1:8000/ to view recent receipts, receipt files, and basic statistics (total receipts, total amount, valid files, processed files).
Admin Interface: Access at http://127.0.0.1:8000/admin/ using the superuser credentials to manage ReceiptFile and Receipt models.
API Endpoints: Use the following endpoints to interact with the application programmatically (see below for details).

API Endpoints
The application provides REST API endpoints for managing receipt files. Use tools like curl or Postman to test them.
1. Upload Receipt
Upload a PDF receipt file.
curl -X POST http://127.0.0.1:8000/upload/ -F "file=@path/to/receipt.pdf"

Response:
{
  "id": 1,
  "file_name": "receipt.pdf",
  "file_path": "/path/to/receipts_data/receipt.pdf",
  "is_valid": false,
  "invalid_reason": null,
  "is_processed": false,
  "created_at": "2025-06-01T15:19:00Z",
  "updated_at": "2025-06-01T15:19:00Z"
}

2. Validate Receipt
Validate a PDF file to check if it’s a valid PDF.
curl -X POST http://127.0.0.1:8000/validate/ -H "Content-Type: application/json" -d '{"file_id": 1}'

Response (Success):
{
  "id": 1,
  "file_name": "receipt.pdf",
  "file_path": "/path/to/receipts_data/receipt.pdf",
  "is_valid": true,
  "invalid_reason": null,
  "is_processed": false,
  "created_at": "2025-06-01T15:19:00Z",
  "updated_at": "2025-06-01T15:20:00Z"
}

Response (Invalid PDF):
{
  "id": 1,
  "file_name": "receipt.pdf",
  "file_path": "/path/to/receipts_data/receipt.pdf",
  "is_valid": false,
  "invalid_reason": "Invalid PDF structure",
  "is_processed": false,
  "created_at": "2025-06-01T15:19:00Z",
  "updated_at": "2025-06-01T15:20:00Z"
}

3. Process Receipt
Extract details (merchant name, total amount, purchase date) from a valid PDF.
curl -X POST http://127.0.0.1:8000/process/ -H "Content-Type: application/json" -d '{"file_id": 1}'

Response:
{
  "id": 1,
  "receipt_file": 1,
  "purchased_at": "2025-06-01T10:00:00Z",
  "merchant_name": "Example Store",
  "total_amount": "25.99",
  "file_path": "/path/to/receipts_data/receipt.pdf",
  "created_at": "2025-06-01T15:21:00Z",
  "updated_at": "2025-06-01T15:21:00Z"
}

Error Response (Invalid File):
{
  "error": "File is not valid"
}

4. List All Receipts
Retrieve a list of all processed receipts.
curl http://127.0.0.1:8000/receipts/

Response:
[
  {
    "id": 1,
    "receipt_file": 1,
    "purchased_at": "2025-06-01T10:00:00Z",
    "merchant_name": "Example Store",
    "total_amount": "25.99",
    "file_path": "/path/to/receipts_data/receipt.pdf",
    "created_at": "2025-06-01T15:21:00Z",
    "updated_at": "2025-06-01T15:21:00Z"
  }
]

5. Get Specific Receipt
Retrieve details of a specific receipt by ID.
curl http://127.0.0.1:8000/receipts/1/

Response:
{
  "id": 1,
  "receipt_file": 1,
  "purchased_at": "2025-06-01T10:00:00Z",
  "merchant_name": "Example Store",
  "total_amount": "25.99",
  "file_path": "/path/to/receipts_data/receipt.pdf",
  "created_at": "2025-06-01T15:21:00Z",
  "updated_at": "2025-06-01T15:21:00Z"
}

6. Delete Receipt
Delete a specific receipt by ID.
curl -X DELETE http://127.0.0.1:8000/receipts/1/delete/

Response:
{
  "message": "Receipt deleted successfully"
}

7. Auto Scan and Process
Scan the receipts_data/ directory and process all PDF files.
curl -X POST http://127.0.0.1:8000/auto-scan/

Response:
{
  "message": "Scanned 5 files, processed 4 receipts",
  "processed_count": 4,
  "total_files": 5,
  "errors": ["Error processing invalid.pdf: Invalid PDF structure"]
}

8. Receipt Statistics
Get basic statistics about receipts.
curl http://127.0.0.1:8000/statistics/

Response:
{
  "total_receipts": 10,
  "total_amount": 250.75
}

Testing the Implementation

Prepare a Test PDF:

Place a sample receipt PDF in the receipts_data/ directory or upload via the /upload/ endpoint.
Ensure the PDF contains extractable text or images with merchant name, total amount, and purchase date.


Test Upload:

Use the curl command for /upload/ to upload a PDF and verify the response contains the file metadata.


Test Validation:

Use the /validate/ endpoint with the returned file_id to check if the PDF is valid.


Test Processing:

Use the /process/ endpoint to extract details and verify the Receipt record is created.


Test Auto-Scan:

Place multiple PDFs in receipts_data/ and use the /auto-scan/ endpoint to process them in bulk.


Test Dashboard:

Open http://127.0.0.1:8000/ in a browser to view the dashboard, ensuring it displays recent receipts and statistics.


Test Admin Interface:

Log in to http://127.0.0.1:8000/admin/ to inspect ReceiptFile and Receipt records.



Troubleshooting

Tesseract/Poppler Errors: Ensure Tesseract and Poppler are installed and added to the system PATH.
PDF Processing Fails: Verify PDFs are not corrupted and contain extractable text or clear images.
Database Issues: Run python manage.py migrate to ensure the database schema is applied.
Server Errors: Check the server logs (python manage.py runserver) for detailed error messages.

Notes

The application uses SQLite (db.sqlite3) for simplicity. Ensure write permissions for the database file.
The dashboard.html template is assumed to exist in the templates/ directory. Create a basic template if needed.
API endpoints assume no authentication for simplicity. Add authentication (e.g., Django REST Framework’s token authentication) for production use.

