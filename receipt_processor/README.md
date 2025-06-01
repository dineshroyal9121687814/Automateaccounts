```markdown
```
## Receipt Processor

A Django-based application for processing receipt PDF files, extracting key details (merchant name, total amount, purchase date), and managing them via a REST API and web dashboard. The application uses SQLite as the database and supports uploading, validating, and processing PDF receipts.
```
```
## Project Structure

- `manage.py`: Django management script.
- `receipt_processor/`: Django project directory containing settings and URLs.
- `receipts/`: Application directory with models, views, serializers, and services.
- `receipts_data/`: Directory for storing uploaded PDF receipt files.
- `db.sqlite3`: SQLite database file.
- `requirements.txt`: Python dependencies.
- `venv/`: Virtual environment directory.
```
```

## Setup Instructions
1. **Clone the Repository or Navigate to Project Directory**
   ```bash
   cd receipt_processor
   ```

2. **Set Up Virtual Environment**
   Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate 
   ```

3. **Install Dependencies**
   Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

   **requirements.txt**:
   ```
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
   ```

4. **Configure Django Settings**
   Ensure `settings.py` in `receipt_processor/` includes:
   ```python
   RECEIPTS_DATA_DIR = os.path.join(BASE_DIR, 'receipts_data')
   ```

5. **Apply Database Migrations**
   Initialize the SQLite database:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create Superuser (Optional)**
   For admin interface access:
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the Development Server**
   Start the Django server:
   ```bash
   python manage.py runserver
   ```
   Access at `http://127.0.0.1:8000/`.

## Running the Application

- **Web Dashboard**: View at `http://127.0.0.1:8000/` to see recent receipts and statistics.
- **Admin Interface**: Access at `http://127.0.0.1:8000/admin/` with superuser credentials.
- **API Endpoints**: Interact programmatically using the endpoints below.

## API Endpoints

Use tools like `curl` or Postman to test the REST API.

1. **Upload and Process Receipt**
   Upload a PDF and extract details (merchant name, total amount, purchase date, items).
   ```bash
   curl -X POST http://127.0.0.1:8000/upload-and-process/ -F "file=@path/to/receipt.pdf"
   ```
   **Response** (Success):
   ```json
   {
     "id": 1,
     "receipt_file": 1,
     "purchased_at": "2025-06-01T10:00:00Z",
     "merchant_name": "Sample Merchant",
     "total_amount": "100.00",
     "file_path": "/path/to/receipts_data/receipt.pdf",
     "extracted_text": "Sample extracted text",
     "category": "Uncategorized",
     "created_at": "2025-06-01T15:19:00Z",
     "updated_at": "2025-06-01T15:19:00Z",
     "items": [
       {"item_name": "Item 1", "quantity": 2, "unit_price": "25.00", "total_price": "50.00"},
       {"item_name": "Item 2", "quantity": 1, "unit_price": "50.00", "total_price": "50.00"}
     ]
   }
   ```
   **Response** (Error):
   ```json
   {"error": "No file provided"}
   ```

2. **List All Receipts**
   Retrieve a list of processed receipts with optional filtering by merchant or category.
   ```bash
   curl http://127.0.0.1:8000/receipts/?merchant=Sample&category=Grocery
   ```
   **Response**:
   ```json
   [
     {
       "id": 1,
       "merchant_name": "Sample Merchant",
       "total_amount": "100.00",
       "purchased_at": "2025-06-01T10:00:00Z",
       "category": "Grocery",
       "created_at": "2025-06-01T15:19:00Z"
     }
   ]
   ```

3. **Receipt Statistics**
   Get statistics (total receipts, total amount, category breakdown).
   ```bash
   curl http://127.0.0.1:8000/statistics/
   ```
   **Response**:
   ```json
   {
     "total_receipts": 10,
     "total_amount": 250.75,
     "by_category": [
       {"category": "Grocery", "count": 5, "total": 150.50},
       {"category": "Restaurant", "count": 3, "total": 80.25}
     ]
   }
   ```

## Testing the Implementation

1. **Prepare a Test PDF**
   - Place a sample receipt PDF in `receipts_data/` or upload via the `/upload-and-process/` endpoint.
   - Ensure the PDF contains extractable text or clear images with merchant name, total amount, and purchase date.

2. **Test Upload and Processing**
   - Use the `/upload-and-process/` endpoint to upload a PDF and verify the response includes extracted details.

3. **Test Listing**
   - Use the `/receipts/` endpoint to list receipts and test filtering by merchant or category.

4. **Test Statistics**
   - Use the `/statistics/` endpoint to verify aggregated data.

5. **Test Dashboard**
   - Open `http://127.0.0.1:8000/` to view the dashboard with recent receipts and stats.

6. **Test Admin Interface**
   - Log in to `http://127.0.0.1:8000/admin/` to manage `ReceiptFile`, `Receipt`, and `ReceiptItem` records.

## Troubleshooting

- **Tesseract/Poppler Errors**: Ensure Tesseract and Poppler are installed and in the system PATH.
- **PDF Processing Fails**: Verify PDFs are not corrupted and contain extractable text or clear images.
- **Database Issues**: Run `python manage.py migrate` to apply the schema.
- **Server Errors**: Check server logs (`python manage.py runserver`) for details.

## Notes

- **Database**: Uses SQLite (`db.sqlite3`) for simplicity. Ensure write permissions for the database file.
- **Templates**: Assumes `dashboard.html` exists in `templates/`. Create a basic template if needed.
- **Authentication**: API endpoints are unauthenticated for simplicity. Add Django REST Framework authentication for production.
- **ReceiptProcessor**: The application assumes a `ReceiptProcessor` class for PDF validation and extraction. Implement or replace with actual logic.

```
