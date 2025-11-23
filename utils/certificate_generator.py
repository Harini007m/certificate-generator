"""
Certificate Generator Module
Generates certificates by overlaying student data on templates.
"""

import os
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.utils import ImageReader
from PyPDF2 import PdfReader, PdfWriter
import io


class CertificateGenerator:
    """Generate certificates from templates and student data."""

    def __init__(self, template_path, output_folder):
        """
        Initialize certificate generator.
        
        Args:
            template_path: Path to certificate template
            output_folder: Folder to save generated certificates
        """
        self.template_path = template_path
        self.output_folder = output_folder
        self.template_extension = os.path.splitext(template_path)[1].lower()

    def generate_certificates(self, students):
        """
        Generate certificates for all students.
        
        Args:
            students: List of student dictionaries
            
        Returns:
            List of certificate information dictionaries
        """
        certificates = []

        for i, student in enumerate(students):
            certificate_path = self._generate_single_certificate(student, i)
            certificates.append({
                'student_name': student['name'],
                'path': certificate_path,
                'filename': os.path.basename(certificate_path)
            })

        return certificates

    def _generate_single_certificate(self, student, index):
        """Generate a single certificate for a student."""
        if self.template_extension in ['.png', '.jpg', '.jpeg']:
            return self._generate_from_image(student, index)
        elif self.template_extension == '.pdf':
            return self._generate_from_pdf(student, index)
        else:
            raise ValueError(f"Unsupported template format: {self.template_extension}")

    def _generate_from_image(self, student, index):
        """Generate certificate from image template."""
        # Open template image
        template = Image.open(self.template_path)
        
        # Create a copy to draw on
        certificate = template.copy()
        draw = ImageDraw.Draw(certificate)

        # Get image dimensions
        width, height = certificate.size

        # Try to load a font, fallback to default if not available
        try:
            # Try different font sizes and styles
            name_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
            detail_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 40)
        except:
            # Fallback to default font
            name_font = ImageFont.load_default()
            detail_font = ImageFont.load_default()

        # Calculate positions (centered)
        # Name position - centered, slightly above middle
        name_text = student['name']
        name_bbox = draw.textbbox((0, 0), name_text, font=name_font)
        name_width = name_bbox[2] - name_bbox[0]
        name_x = (width - name_width) // 2
        name_y = int(height * 0.45)

        # Department position
        dept_text = f"Department: {student['department']}"
        dept_bbox = draw.textbbox((0, 0), dept_text, font=detail_font)
        dept_width = dept_bbox[2] - dept_bbox[0]
        dept_x = (width - dept_width) // 2
        dept_y = int(height * 0.60)

        # Class position
        class_text = f"Class: {student['class']}"
        class_bbox = draw.textbbox((0, 0), class_text, font=detail_font)
        class_width = class_bbox[2] - class_bbox[0]
        class_x = (width - class_width) // 2
        class_y = int(height * 0.68)

        # Draw text on certificate
        draw.text((name_x, name_y), name_text, fill='black', font=name_font)
        draw.text((dept_x, dept_y), dept_text, fill='black', font=detail_font)
        draw.text((class_x, class_y), class_text, fill='black', font=detail_font)

        # Convert to PDF
        output_filename = f"certificate_{index + 1}_{student['name'].replace(' ', '_')}.pdf"
        output_path = os.path.join(self.output_folder, output_filename)

        # Save as PDF using ReportLab
        pdf_buffer = io.BytesIO()
        c = canvas.Canvas(pdf_buffer, pagesize=(width, height))
        
        # Convert PIL image to ReportLab ImageReader
        img_buffer = io.BytesIO()
        certificate.save(img_buffer, format='PNG')
        img_buffer.seek(0)
        img_reader = ImageReader(img_buffer)
        
        c.drawImage(img_reader, 0, 0, width, height)
        c.save()

        # Write PDF to file
        with open(output_path, 'wb') as f:
            f.write(pdf_buffer.getvalue())

        return output_path

    def _generate_from_pdf(self, student, index):
        """Generate certificate from PDF template."""
        # Read the template PDF
        reader = PdfReader(self.template_path)
        writer = PdfWriter()

        # Get the first page
        page = reader.pages[0]
        
        # Get page dimensions
        page_box = page.mediabox
        page_width = float(page_box.width)
        page_height = float(page_box.height)

        # Create overlay with text
        packet = io.BytesIO()
        c = canvas.Canvas(packet, pagesize=(page_width, page_height))

        # Set font
        c.setFont("Helvetica-Bold", 36)
        
        # Calculate positions (centered)
        # Name position
        name_text = student['name']
        name_width = c.stringWidth(name_text, "Helvetica-Bold", 36)
        name_x = (page_width - name_width) / 2
        name_y = page_height * 0.55

        c.drawString(name_x, name_y, name_text)

        # Department
        c.setFont("Helvetica", 24)
        dept_text = f"Department: {student['department']}"
        dept_width = c.stringWidth(dept_text, "Helvetica", 24)
        dept_x = (page_width - dept_width) / 2
        dept_y = page_height * 0.40

        c.drawString(dept_x, dept_y, dept_text)

        # Class
        class_text = f"Class: {student['class']}"
        class_width = c.stringWidth(class_text, "Helvetica", 24)
        class_x = (page_width - class_width) / 2
        class_y = page_height * 0.32

        c.drawString(class_x, class_y, class_text)

        c.save()

        # Move to the beginning of the StringIO buffer
        packet.seek(0)
        overlay_pdf = PdfReader(packet)

        # Merge the overlay with the template
        page.merge_page(overlay_pdf.pages[0])
        writer.add_page(page)

        # Add remaining pages if any
        for page_num in range(1, len(reader.pages)):
            writer.add_page(reader.pages[page_num])

        # Write output
        output_filename = f"certificate_{index + 1}_{student['name'].replace(' ', '_')}.pdf"
        output_path = os.path.join(self.output_folder, output_filename)

        with open(output_path, 'wb') as output_file:
            writer.write(output_file)

        return output_path
