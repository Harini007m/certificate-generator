# Setup Guide

This guide will help you set up the Certificate Generator on your system.

## Quick Start

### 1. Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### 2. Installation Steps

```bash
# Clone the repository
git clone https://github.com/Harini007m/certificate-generator.git
cd certificate-generator

# Create and activate virtual environment
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment (optional for basic use)
cp .env.example .env
# Edit .env with your settings (optional)

# Run the application
python app.py
```

### 3. Access the Application

Open your web browser and navigate to:
```
http://localhost:5000
```

## Configuration

### Environment Variables

The application can run without any configuration, but you can customize it by creating a `.env` file:

```bash
cp .env.example .env
```

Then edit `.env` with your preferred settings:

#### Required for Production
- `FLASK_SECRET_KEY`: A secure random string for session management
  - Generate one: `python -c "import secrets; print(secrets.token_hex(32))"`

#### Optional Email Configuration
- `SENDGRID_API_KEY`: Your SendGrid API key (for actual email sending)
- `TWILIO_FROM_EMAIL`: Verified sender email address
- `TWILIO_ACCOUNT_SID`: Twilio account SID (optional)
- `TWILIO_AUTH_TOKEN`: Twilio auth token (optional)

#### Optional Application Settings
- `FLASK_DEBUG`: Set to `True` for development, `False` for production (default: False)
- `UPLOAD_FOLDER`: Directory for uploaded files (default: uploads)
- `CERTIFICATES_FOLDER`: Directory for generated certificates (default: generated_certificates)
- `MAX_CONTENT_LENGTH`: Maximum upload size in bytes (default: 16MB)

### Email Setup

The application works in **simulation mode** by default, which means:
- Certificates are generated normally
- "Email sending" is simulated (logged to console)
- No actual emails are sent

To enable **actual email sending**:

1. Sign up for SendGrid (recommended): https://sendgrid.com/
2. Get your API key
3. Install the sendgrid package:
   ```bash
   pip install sendgrid
   ```
4. Uncomment the SendGrid code in `utils/email_sender.py`
5. Add your API key to `.env`:
   ```
   SENDGRID_API_KEY=your_actual_api_key_here
   ```

## Testing the Installation

Run the test script to verify everything is working:

```bash
python test_system.py
```

You should see all tests pass:
```
✓ All tests passed!
```

## Usage

### Step 1: Prepare Your Files

#### Certificate Template
- Format: PNG, JPG, JPEG, or PDF
- Recommended size: 1920x1080 pixels (landscape) or A4
- Leave space for text in the center

#### Student Data File
- Format: Excel (.xlsx, .xls), CSV, or DOCX
- Required columns: `Name`, `Department`, `Class`
- Optional column: `Email` (for sending certificates)

Example CSV format:
```csv
Name,Department,Class,Email
John Doe,Computer Science,2023,john@example.com
Jane Smith,Electrical Engineering,2024,jane@example.com
```

See `examples/sample_students.csv` for a complete example.

### Step 2: Use the Web Interface

1. **Upload Files**: Select your template and student data file
2. **Review Students**: Verify the parsed student information
3. **Generate Certificates**: Click to generate all certificates
4. **Preview & Download**: Preview each certificate before sending
5. **Send Emails** (Optional): Send certificates to students with email addresses

## Troubleshooting

### Common Issues

#### ImportError or ModuleNotFoundError
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

#### Port Already in Use
If port 5000 is already in use, modify `app.py`:
```python
app.run(debug=debug_mode, host='0.0.0.0', port=8080)  # Change port
```

#### Font Not Found Warnings
The application will fall back to default fonts if system fonts are not found. This is normal and won't affect certificate generation.

#### File Upload Fails
- Check file size (default limit: 16MB)
- Verify file format is supported
- Ensure proper column names in student data file

#### Email Simulation Mode
If you see "simulation mode" messages, this is normal behavior when email credentials are not configured. Certificates are still generated successfully.

## Production Deployment

For production deployment:

1. **Use a Production Server**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

2. **Set Production Environment Variables**
   ```bash
   export FLASK_SECRET_KEY="your-secure-random-key"
   export FLASK_DEBUG="False"
   ```

3. **Use HTTPS** (with reverse proxy like nginx)

4. **Configure Email** (with actual SendGrid API key)

5. **Set Up Proper File Permissions**
   ```bash
   chmod 755 uploads generated_certificates
   ```

## Security Considerations

- Never commit `.env` file to version control
- Use strong, random `FLASK_SECRET_KEY` in production
- Keep `FLASK_DEBUG=False` in production
- Validate and sanitize all file uploads
- Use HTTPS in production
- Regularly update dependencies

## Getting Help

- Check the [README.md](README.md) for detailed documentation
- Review [examples/](examples/) directory for sample files
- Run `python test_system.py` to diagnose issues
- Open an issue on GitHub for bugs or feature requests

## Next Steps

After successful setup:
1. Try the example files in `examples/` directory
2. Create your own certificate template
3. Prepare your student data file
4. Generate your first batch of certificates!
