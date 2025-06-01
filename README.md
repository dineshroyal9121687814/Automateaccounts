# Receipt Processor

A Django-based application for processing receipt PDF files, extracting key details (merchant name, total amount, purchase date), and managing them via a REST API and web dashboard. The application uses SQLite as the database and supports uploading, validating, and processing PDF receipts.

## Project Structure

- `manage.py`: Django management script.
- `receipt_processor/`: Django project directory containing settings and URLs.
- `receipts/`: Application directory with models, views, serializers, and services.
- `receipts_data/`: Directory for storing uploaded PDF receipt files.
- `db.sqlite3`: SQLite database file.
- `requirements.txt`: Python dependencies.
- `venv/`: Virtual environment directory.

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

## API Endpoints

Use tools like `curl` or Postman to test the REST API.

1. **Upload Receipt**
   Upload a PDF file to store and prepare for validation:
   ```bash
   curl -X POST http://127.0.0.1:8000/upload/      -F "file=@receipt.pdf"
   ```

2. **Validate Receipt**
   Run validation checks (e.g. format, readability) on uploaded file:
   ```bash
   curl -X POST http://127.0.0.1:8000/validate/      -H "Content-Type: application/json"      -d '{"file_id": 1}'
   ```

3. **Process Receipt**
   Extract key information from the receipt:
   ```bash
   curl -X POST http://127.0.0.1:8000/process/      -H "Content-Type: application/json"      -d '{"file_id": 1}'
   ```

4. **List All Receipts**
   Retrieve a list of all processed receipts:
   ```bash
   curl http://127.0.0.1:8000/receipts/
   ```

5. **Get Specific Receipt**
   Fetch details of a specific receipt by its ID:
   ```bash
   curl http://127.0.0.1:8000/receipts/1/
   ```

## Testing the Implementation

1. **Prepare a Test PDF**
   - Place a sample receipt PDF in `receipts_data/` or upload via the `/upload/` endpoint.
   - Ensure the PDF contains extractable text or clear images with merchant name, total amount, and purchase date.

2. **Test Upload, Validation, and Processing**
   - Use the `/upload/`, `/validate/`, and `/process/` endpoints and verify responses include extracted details.

3. **Test Listing**
   - Use the `/receipts/` endpoint to list receipts.

4. **Test Admin Interface**
   - Log in to `http://127.0.0.1:8000/admin/` to manage `ReceiptFile`, `Receipt`, and `ReceiptItem` records.

## Troubleshooting

- **PDF Processing Fails**: Verify PDFs are not corrupted and contain extractable text or clear images.
- **Database Issues**: Run `python manage.py migrate` to apply the schema.
- **Server Errors**: Check server logs (`python manage.py runserver`) for details.
