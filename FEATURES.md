# Certificate Generator - Feature Documentation

## Overview

This certificate generator system automates the process of creating personalized certificates for students. It accepts a certificate template and a list of students, then generates individualized certificates by overlaying student information on the template.

## Core Features

### 1. Multi-Format File Upload

**Certificate Templates:**
- PNG images
- JPG/JPEG images
- PDF documents

**Student Data:**
- Excel spreadsheets (.xlsx, .xls)
- CSV files
- Microsoft Word documents (.docx)

**Note:** Legacy .doc format is not supported due to library limitations.

### 2. Intelligent Data Parsing

The system automatically recognizes various column naming conventions:

- **Name**: `name`, `student_name`, `student name`, `full_name`, `full name`, `studentname`
- **Department**: `department`, `dept`, `branch`, `stream`, `course`
- **Class**: `class`, `year`, `semester`, `grade`, `level`, `section`
- **Email**: `email`, `email_address`, `email address`, `mail`, `e-mail`

This flexibility allows users to upload data files without strict formatting requirements.

### 3. Certificate Generation

**Image Templates (PNG/JPG):**
- Opens the template image
- Overlays student information with proper formatting
- Centered text placement:
  - Name: 45% from top (large, bold font)
  - Department: 60% from top (medium font)
  - Class: 68% from top (medium font)
- Converts to PDF for consistent output

**PDF Templates:**
- Reads existing PDF template
- Merges text overlay with template
- Maintains original template quality
- Adds text at calculated center positions

**Cross-Platform Font Support:**
- Automatically detects system fonts (Linux, macOS, Windows)
- Falls back to default fonts if system fonts unavailable
- No manual font installation required

### 4. Preview & Verification

- Preview each certificate before sending
- Download individual certificates
- Verify all student details are accurate
- Ensure proper text placement and formatting

### 5. Email Integration

**Simulation Mode (Default):**
- No configuration required
- Logs email operations to console
- Certificates still generated normally
- Perfect for testing and development

**Production Mode (Optional):**
- Integrates with SendGrid API
- Sends certificates as email attachments
- Customizable email messages
- Professional email formatting
- Bulk sending to multiple recipients

### 6. User-Friendly Web Interface

**Three-Step Workflow:**

1. **Upload Files**
   - Select certificate template
   - Choose student data file
   - Automatic validation

2. **Review Students**
   - View parsed student information
   - Verify data accuracy
   - See student count

3. **Preview & Send**
   - Preview each certificate
   - Download certificates individually
   - Add custom email message
   - Send to all students with emails

**Modern UI Design:**
- Gradient background design
- Responsive layout (mobile-friendly)
- Loading indicators
- Success/error notifications
- Clean, professional appearance

## Technical Features

### Security

- ✅ No debug mode in production
- ✅ Secure session management
- ✅ File upload validation
- ✅ Input sanitization
- ✅ Environment-based configuration
- ✅ No hardcoded secrets
- ✅ Passed CodeQL security scan

### Error Handling

- Specific exception types
- Graceful fallbacks
- User-friendly error messages
- Detailed logging
- Validation at each step

### Scalability

- Session-based workflow
- Efficient file handling
- Modular architecture
- Easy to extend
- Well-documented code

### Cross-Platform Compatibility

- Works on Linux, macOS, Windows
- Automatic font detection
- Path handling for all OS
- Virtual environment support

## File Structure

```
certificate-generator/
├── app.py                     # Flask application (API endpoints)
├── utils/
│   ├── file_parser.py        # Parse Excel/CSV/DOCX files
│   ├── certificate_generator.py  # Generate certificates
│   └── email_sender.py       # Send emails via Twilio/SendGrid
├── templates/
│   └── index.html            # Web interface
├── static/
│   ├── css/style.css         # Styling
│   └── js/script.js          # Frontend logic
├── examples/
│   ├── sample_students.csv   # Example data file
│   └── README.md             # Example documentation
├── requirements.txt          # Python dependencies
├── .env.example              # Configuration template
├── .gitignore                # Git ignore rules
├── README.md                 # Main documentation
├── SETUP.md                  # Setup guide
├── FEATURES.md               # This file
├── LICENSE                   # MIT License
└── test_system.py            # System tests
```

## API Endpoints

### `POST /upload`
Uploads template and student data files.

**Request:** `multipart/form-data`
- `template`: Certificate template file
- `student_data`: Student information file

**Response:** Student count and parsed data

### `POST /generate`
Generates certificates for all students.

**Response:** List of generated certificates with paths

### `GET /preview/<index>`
Preview a specific certificate.

**Response:** PDF file for preview

### `GET /download/<index>`
Download a specific certificate.

**Response:** PDF file as attachment

### `POST /send_emails`
Send certificates via email.

**Request:** `application/json`
- `message`: Custom email message (optional)

**Response:** Email sending results

## Dependencies

- **Flask 3.0.0**: Web framework
- **Pillow 10.1.0**: Image processing
- **pandas 2.1.3**: Data parsing
- **openpyxl 3.1.2**: Excel file support
- **python-docx 1.1.0**: Word document support
- **reportlab 4.0.7**: PDF generation
- **PyPDF2 3.0.1**: PDF manipulation
- **twilio 8.10.0**: Email integration
- **python-dotenv 1.0.0**: Environment configuration
- **xlrd 2.0.1**: Legacy Excel support

## Configuration Options

All configuration is optional and can be set via environment variables:

| Variable | Purpose | Default |
|----------|---------|---------|
| `FLASK_SECRET_KEY` | Session security | Auto-generated |
| `FLASK_DEBUG` | Debug mode | False |
| `SENDGRID_API_KEY` | Email API key | None (simulation) |
| `TWILIO_FROM_EMAIL` | Sender email | None |
| `UPLOAD_FOLDER` | Upload directory | uploads |
| `CERTIFICATES_FOLDER` | Output directory | generated_certificates |
| `MAX_CONTENT_LENGTH` | Max file size | 16MB |

## Use Cases

1. **Educational Institutions**
   - Course completion certificates
   - Award certificates
   - Participation certificates

2. **Corporate Training**
   - Training completion certificates
   - Workshop attendance
   - Skill certifications

3. **Events & Competitions**
   - Event participation
   - Winner certificates
   - Speaker recognition

4. **Online Courses**
   - Course completion
   - Assessment certificates
   - Skill badges

## Future Enhancement Possibilities

- Support for multiple certificate templates
- Custom text positioning configuration
- Certificate design preview before generation
- Bulk operations with progress tracking
- Certificate templates library
- Database integration for student records
- API for programmatic access
- Internationalization support
- Custom fonts upload
- QR code integration for verification
- Certificate numbering and tracking
- Analytics and reporting
- Scheduled email sending

## Performance

- Handles multiple students efficiently
- Supports concurrent requests
- Memory-efficient file handling
- Fast PDF generation
- Optimized image processing

## Limitations

- Maximum file upload size: 16MB (configurable)
- Legacy .doc format not supported
- Email requires external service (SendGrid)
- Single template per batch
- Text positioning is predefined

## Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Review documentation (README.md, SETUP.md)
- Run test suite (test_system.py)
- Check examples directory

## License

This project is licensed under the MIT License. See LICENSE file for details.
