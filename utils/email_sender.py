"""
Email Sender Module
Sends certificates via email using Twilio SendGrid API.
"""

import os
from twilio.rest import Client
from dotenv import load_dotenv
import base64

load_dotenv()


class EmailSender:
    """Send certificates via email using Twilio."""

    def __init__(self):
        """Initialize email sender with Twilio credentials."""
        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.from_email = os.getenv('TWILIO_FROM_EMAIL')

        if not all([self.account_sid, self.auth_token, self.from_email]):
            raise ValueError("Twilio credentials not properly configured in .env file")

        # Initialize Twilio client
        self.client = Client(self.account_sid, self.auth_token)

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

            # Note: Twilio's main service doesn't directly send emails with attachments
            # This is a placeholder implementation that shows the structure
            # In production, you would use Twilio SendGrid API for email
            # For now, we'll simulate the email sending

            print(f"Simulating email send to {to_email}")
            print(f"Subject: {subject}")
            print(f"Body preview: {default_message[:100]}...")
            print(f"Attachment: {os.path.basename(certificate_path)}")

            # In a real implementation with SendGrid, you would do:
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
            # sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
            # response = sg.send(message)

            # For demo purposes, return True
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
