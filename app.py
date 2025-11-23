"""
Certificate Generator Application
Main Flask application for generating certificates from templates and student data.
"""

import os
from flask import Flask, render_template, request, jsonify, send_file, session
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import json

from utils.file_parser import FileParser
from utils.certificate_generator import CertificateGenerator
from utils.email_sender import EmailSender

# Load environment variables
load_dotenv()

app = Flask(__name__)
secret_key = os.getenv('FLASK_SECRET_KEY')
if not secret_key:
    import secrets
    secret_key = secrets.token_hex(32)
    print("WARNING: FLASK_SECRET_KEY not set in environment. Using generated key for this session.")
app.config['SECRET_KEY'] = secret_key
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'uploads')
app.config['CERTIFICATES_FOLDER'] = os.getenv('CERTIFICATES_FOLDER', 'generated_certificates')
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))  # 16MB

# Create necessary directories
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['CERTIFICATES_FOLDER'], exist_ok=True)

# Allowed file extensions
ALLOWED_TEMPLATE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}
ALLOWED_DATA_EXTENSIONS = {'xlsx', 'xls', 'csv', 'docx'}


def allowed_file(filename, allowed_extensions):
    """Check if file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_files():
    """Handle file uploads for template and student data."""
    try:
        # Check if files are present
        if 'template' not in request.files or 'student_data' not in request.files:
            return jsonify({'error': 'Both template and student data files are required'}), 400

        template_file = request.files['template']
        data_file = request.files['student_data']

        # Validate files
        if template_file.filename == '' or data_file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        if not allowed_file(template_file.filename, ALLOWED_TEMPLATE_EXTENSIONS):
            return jsonify({'error': 'Invalid template file format. Allowed: PNG, JPG, JPEG, PDF'}), 400

        if not allowed_file(data_file.filename, ALLOWED_DATA_EXTENSIONS):
            return jsonify({'error': 'Invalid data file format. Allowed: XLSX, XLS, CSV, DOCX'}), 400

        # Save files
        template_filename = secure_filename(template_file.filename)
        data_filename = secure_filename(data_file.filename)

        template_path = os.path.join(app.config['UPLOAD_FOLDER'], template_filename)
        data_path = os.path.join(app.config['UPLOAD_FOLDER'], data_filename)

        template_file.save(template_path)
        data_file.save(data_path)

        # Parse student data
        file_parser = FileParser()
        students = file_parser.parse_file(data_path)

        if not students:
            return jsonify({'error': 'No valid student data found in the file'}), 400

        # Store paths in session
        session['template_path'] = template_path
        session['data_path'] = data_path
        session['students'] = students

        return jsonify({
            'message': 'Files uploaded successfully',
            'student_count': len(students),
            'students': students
        }), 200

    except Exception as e:
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500


@app.route('/generate', methods=['POST'])
def generate_certificates():
    """Generate certificates for all students."""
    try:
        template_path = session.get('template_path')
        students = session.get('students')

        if not template_path or not students:
            return jsonify({'error': 'Please upload files first'}), 400

        # Generate certificates
        generator = CertificateGenerator(template_path, app.config['CERTIFICATES_FOLDER'])
        certificates = generator.generate_certificates(students)

        # Store certificate info in session
        session['certificates'] = certificates

        return jsonify({
            'message': 'Certificates generated successfully',
            'certificates': certificates
        }), 200

    except Exception as e:
        return jsonify({'error': f'Certificate generation failed: {str(e)}'}), 500


@app.route('/preview/<int:index>')
def preview_certificate(index):
    """Preview a specific certificate."""
    try:
        certificates = session.get('certificates', [])
        if index < 0 or index >= len(certificates):
            return jsonify({'error': 'Invalid certificate index'}), 400

        certificate_path = certificates[index]['path']
        if not os.path.exists(certificate_path):
            return jsonify({'error': 'Certificate file not found'}), 404

        return send_file(certificate_path, mimetype='application/pdf')

    except Exception as e:
        return jsonify({'error': f'Preview failed: {str(e)}'}), 500


@app.route('/send_emails', methods=['POST'])
def send_emails():
    """Send certificates via email using Twilio."""
    try:
        students = session.get('students', [])
        certificates = session.get('certificates', [])

        if not students or not certificates:
            return jsonify({'error': 'Please generate certificates first'}), 400

        # Get custom message from request
        data = request.get_json()
        custom_message = data.get('message', '')

        # Initialize email sender
        email_sender = EmailSender()

        # Send emails
        results = []
        for i, (student, certificate) in enumerate(zip(students, certificates)):
            if 'email' in student and student['email']:
                result = email_sender.send_certificate(
                    student['email'],
                    student['name'],
                    certificate['path'],
                    custom_message
                )
                results.append({
                    'student': student['name'],
                    'email': student['email'],
                    'status': 'sent' if result else 'failed'
                })
            else:
                results.append({
                    'student': student['name'],
                    'email': 'N/A',
                    'status': 'no_email'
                })

        return jsonify({
            'message': 'Email sending completed',
            'results': results
        }), 200

    except Exception as e:
        return jsonify({'error': f'Email sending failed: {str(e)}'}), 500


@app.route('/download/<int:index>')
def download_certificate(index):
    """Download a specific certificate."""
    try:
        certificates = session.get('certificates', [])
        if index < 0 or index >= len(certificates):
            return jsonify({'error': 'Invalid certificate index'}), 400

        certificate = certificates[index]
        certificate_path = certificate['path']
        
        if not os.path.exists(certificate_path):
            return jsonify({'error': 'Certificate file not found'}), 404

        return send_file(
            certificate_path,
            as_attachment=True,
            download_name=os.path.basename(certificate_path)
        )

    except Exception as e:
        return jsonify({'error': f'Download failed: {str(e)}'}), 500


if __name__ == '__main__':
    # Only enable debug mode in development environment
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
