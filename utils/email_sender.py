"""
Email Sender Module
Sends certificates via email using Twilio SendGrid API.

Note: Current implementation simulates email sending for demonstration purposes.
To enable actual email sending, install the sendgrid package and uncomment
the SendGrid integration code in the send_certificate method.

Required package: pip install sendgrid
Environment variable: SENDGRID_API_KEY
"""

import os
from dotenv import load_dotenv
import base64

load_dotenv()


class EmailSender:
    """Send certificates via email using Twilio SendGrid."""

    def __init__(self):
        """Initialize email sender with Twilio/SendGrid credentials."""
        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.from_email = os.getenv('TWILIO_FROM_EMAIL')
        self.sendgrid_api_key = os.getenv('SENDGRID_API_KEY')

        # Allow initialization without credentials for demo mode
        if not all([self.from_email]):
            print("WARNING: Email credentials not configured. Running in simulation mode.")
            self.simulation_mode = True
        else:
            self.simulation_mode = False

    def send_certificate(self, to_email, student_name, certificate_path, custom_message=''):
        """
        Send certificate via email.
        
        Args:
            to_email: Recipient email address
            student_name: Name of the student
            certificate_path: Path to certificate PDF
            custom_message: Custom message to include in email
            
        Returns:
            Boolean indicating success or failure
        """
        try:
            # Prepare email subject
            subject = f"Certificate of Achievement - {student_name}"

            # Prepare email body
            default_message = f"""
Dear {student_name},

Congratulations on your achievement! Please find your certificate attached to this email.

{custom_message}

This certificate recognizes your dedication and accomplishments. We are proud of your success!

Best regards,
Certificate Generation Team
"""

            # Read certificate file
            with open(certificate_path, 'rb') as f:
                certificate_data = f.read()

            # Encode certificate as base64
            certificate_b64 = base64.b64encode(certificate_data).decode('utf-8')

            if self.simulation_mode or not self.sendgrid_api_key:
                # Simulation mode - log the email that would be sent
                print(f"[SIMULATION] Email to: {to_email}")
                print(f"[SIMULATION] Subject: {subject}")
                print(f"[SIMULATION] Attachment: {os.path.basename(certificate_path)}")
                return True
            
            # Real implementation with SendGrid (requires sendgrid package)
            # Uncomment this section and install sendgrid package to enable actual email sending
            #
            # from sendgrid import SendGridAPIClient
            # from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
            # 
            # message = Mail(
            #     from_email=self.from_email,
            #     to_emails=to_email,
            #     subject=subject,
            #     plain_text_content=default_message
            # )
            # 
            # attachment = Attachment(
            #     FileContent(certificate_b64),
            #     FileName(os.path.basename(certificate_path)),
            #     FileType('application/pdf'),
            #     Disposition('attachment')
            # )
            # message.attachment = attachment
            # 
            # sg = SendGridAPIClient(self.sendgrid_api_key)
            # response = sg.send(message)
            # return response.status_code in [200, 201, 202]
            
            return True

        except Exception as e:
            print(f"Error sending email to {to_email}: {str(e)}")
            return False

    def send_bulk_certificates(self, recipients):
        """
        Send certificates to multiple recipients.
        
        Args:
            recipients: List of dictionaries with 'email', 'name', 'certificate_path'
            
        Returns:
            Dictionary with success and failure counts
        """
        results = {'success': 0, 'failed': 0}

        for recipient in recipients:
            success = self.send_certificate(
                recipient['email'],
                recipient['name'],
                recipient['certificate_path']
            )
            
            if success:
                results['success'] += 1
            else:
                results['failed'] += 1

        return results
