# Certificate Generator

An automated certificate generation system that creates personalized certificates for students by overlaying their details (name, department, class) on a certificate template. The system supports multiple input file formats and can send certificates via email.

## Features

- 📁 **Multiple File Format Support**
  - Certificate Templates: PNG, JPG, JPEG, PDF
  - Student Data: Excel (.xlsx, .xls), CSV, DOCX (Note: Legacy .doc format is not supported)

- 🎓 **Automatic Certificate Generation**
  - Extracts student information from uploaded files
  - Overlays name, department, and class on certificate template
  - Generates PDF certificates for each student
  - Centered text positioning for professional appearance

- 👀 **Preview Functionality**
  - Preview each certificate before sending
  - Download individual certificates
  - Verify all details are accurate

- 📧 **Email Integration**
  - Send certificates via email using Twilio
  - Custom message support
  - Proper email formatting with attachments
  - Bulk sending to all students

- 🖥️ **User-Friendly Web Interface**
  - Simple three-step workflow
  - Real-time progress feedback
  - Responsive design

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/Harini007m/certificate-generator.git
cd certificate-generator
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
```

Edit `.env` file and add your Twilio credentials:
```
TWILIO_ACCOUNT_SID=your_account_sid_here
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_FROM_EMAIL=your_verified_sender_email@example.com
FLASK_SECRET_KEY=your_secret_key_here
```

## Usage

### Starting the Application

1. Run the Flask application:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

### Generating Certificates

#### Step 1: Upload Files

1. **Upload Certificate Template**: Select a PNG, JPG, JPEG, or PDF file
   - Template should have space for student name, department, and class
   - Recommended size: 1920x1080 pixels or A4 size

2. **Upload Student Data**: Select an Excel, CSV, DOC, or DOCX file
   - Required columns: `Name`, `Department`, `Class`
   - Optional column: `Email` (for sending certificates)

**Example Excel/CSV Format:**
```
Name                | Department            | Class      | Email
--------------------|----------------------|------------|-------------------------
John Doe            | Computer Science     | 2023       | john@example.com
Jane Smith          | Electrical Engineering| 2024      | jane@example.com
```

**Example DOCX Format (Table):**
```
| Name       | Department           | Class | Email              |
|------------|---------------------|-------|-------------------|
| John Doe   | Computer Science    | 2023  | john@example.com  |
| Jane Smith | Electrical Engineering | 2024 | jane@example.com |
```

#### Step 2: Review Student Data

- Review the parsed student information
- Verify all details are correct
- Click "Generate Certificates" to proceed

#### Step 3: Preview and Send

- Preview each certificate
- Download individual certificates
- Add custom email message (optional)
- Click "Send All Certificates" to email certificates

## File Format Details

### Student Data File Formats

The system is flexible with column names and supports various formats:

**Accepted column names:**
- **Name**: `name`, `student_name`, `student name`, `full_name`, `full name`, `studentname`
- **Department**: `department`, `dept`, `branch`, `stream`, `course`
- **Class**: `class`, `year`, `semester`, `grade`, `level`, `section`
- **Email**: `email`, `email_address`, `email address`, `mail`, `e-mail`

### Certificate Templates

- **Image templates (PNG/JPG)**: The system overlays text on the image at predefined positions
- **PDF templates**: Text is merged with the PDF template

Position defaults (can be customized in code):
- Name: Center, 45% from top (larger font)
- Department: Center, 60% from top
- Class: Center, 68% from top

## Project Structure

```
certificate-generator/
├── app.py                      # Main Flask application
├── utils/
│   ├── __init__.py
│   ├── file_parser.py         # File parsing utilities
│   ├── certificate_generator.py # Certificate generation logic
│   └── email_sender.py        # Email sending with Twilio
├── templates/
│   └── index.html             # Web interface
├── static/
│   ├── css/
│   │   └── style.css         # Styling
│   └── js/
│       └── script.js         # Frontend logic
├── uploads/                   # Uploaded files (created automatically)
├── generated_certificates/    # Generated PDFs (created automatically)
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore rules
└── README.md                 # Documentation
```

## API Endpoints

- `GET /` - Main page
- `POST /upload` - Upload template and student data
- `POST /generate` - Generate certificates
- `GET /preview/<index>` - Preview certificate
- `GET /download/<index>` - Download certificate
- `POST /send_emails` - Send certificates via email

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `TWILIO_ACCOUNT_SID` | Twilio account SID | No (optional) |
| `TWILIO_AUTH_TOKEN` | Twilio auth token | No (optional) |
| `TWILIO_FROM_EMAIL` | Verified sender email | No (optional) |
| `SENDGRID_API_KEY` | SendGrid API key | No (optional) |
| `FLASK_SECRET_KEY` | Flask session secret key | Yes |
| `FLASK_DEBUG` | Enable Flask debug mode (use False in production) | No (default: False) |
| `UPLOAD_FOLDER` | Upload directory | No (default: uploads) |
| `CERTIFICATES_FOLDER` | Generated certificates directory | No (default: generated_certificates) |
| `MAX_CONTENT_LENGTH` | Maximum upload size in bytes | No (default: 16MB) |

## Email Setup (Optional)

The system runs in simulation mode by default. To enable actual email sending:

1. **Option 1: Using SendGrid (Recommended)**
   - Sign up at [SendGrid](https://sendgrid.com/)
   - Get your API key
   - Install sendgrid: `pip install sendgrid`
   - Uncomment the SendGrid code in `utils/email_sender.py`
   - Add `SENDGRID_API_KEY` to `.env` file

2. **Option 2: Using Twilio**
   - Sign up at [Twilio](https://www.twilio.com/)
   - Get your Account SID and Auth Token
   - Set up email integration
   - Add credentials to `.env` file

**Note**: Without these credentials, the system will simulate email sending (logging to console) but still generate certificates normally.

## Troubleshooting

### Common Issues

1. **Font not found**: The system uses DejaVu fonts. If not available, it falls back to default fonts.

2. **Email not sending**: Verify Twilio credentials and ensure sender email is verified.

3. **File parsing errors**: Ensure student data file has the correct format and column names.

4. **Upload size limit**: Increase `MAX_CONTENT_LENGTH` in `.env` for larger files.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.

## Support

For issues and questions, please open an issue on GitHub.

## Acknowledgments

- Flask for the web framework
- Pillow for image processing
- ReportLab for PDF generation
- Twilio for email services
- pandas for data parsing