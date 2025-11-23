// Certificate Generator JavaScript

let studentsData = [];
let certificatesData = [];

// DOM Elements
const uploadForm = document.getElementById('upload-form');
const uploadSection = document.getElementById('upload-section');
const reviewSection = document.getElementById('review-section');
const previewSection = document.getElementById('preview-section');
const generateBtn = document.getElementById('generate-btn');
const sendEmailBtn = document.getElementById('send-email-btn');
const loading = document.getElementById('loading');
const messageContainer = document.getElementById('message-container');

// Event Listeners
uploadForm.addEventListener('submit', handleUpload);
generateBtn.addEventListener('click', generateCertificates);
sendEmailBtn.addEventListener('click', sendEmails);

// Handle file upload
async function handleUpload(e) {
    e.preventDefault();
    
    const formData = new FormData(uploadForm);
    
    showLoading();
    
    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        hideLoading();
        
        if (response.ok) {
            studentsData = data.students;
            showMessage('Files uploaded successfully!', 'success');
            displayStudents(data.students);
            reviewSection.classList.remove('hidden');
        } else {
            showMessage(data.error || 'Upload failed', 'error');
        }
    } catch (error) {
        hideLoading();
        showMessage('Error uploading files: ' + error.message, 'error');
    }
}

// Display students for review
function displayStudents(students) {
    const studentList = document.getElementById('student-list');
    studentList.innerHTML = '';
    
    if (students.length === 0) {
        studentList.innerHTML = '<p>No students found</p>';
        return;
    }
    
    students.forEach((student, index) => {
        const studentDiv = document.createElement('div');
        studentDiv.className = 'student-item';
        studentDiv.innerHTML = `
            <h4>${index + 1}. ${student.name}</h4>
            <p><strong>Department:</strong> ${student.department}</p>
            <p><strong>Class:</strong> ${student.class}</p>
            <p><strong>Email:</strong> ${student.email || 'Not provided'}</p>
        `;
        studentList.appendChild(studentDiv);
    });
}

// Generate certificates
async function generateCertificates() {
    showLoading();
    
    try {
        const response = await fetch('/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        
        hideLoading();
        
        if (response.ok) {
            certificatesData = data.certificates;
            showMessage('Certificates generated successfully!', 'success');
            displayCertificates(data.certificates);
            previewSection.classList.remove('hidden');
        } else {
            showMessage(data.error || 'Certificate generation failed', 'error');
        }
    } catch (error) {
        hideLoading();
        showMessage('Error generating certificates: ' + error.message, 'error');
    }
}

// Display certificates with preview and download options
function displayCertificates(certificates) {
    const certificateList = document.getElementById('certificate-list');
    certificateList.innerHTML = '';
    
    certificates.forEach((cert, index) => {
        const certDiv = document.createElement('div');
        certDiv.className = 'certificate-item';
        certDiv.innerHTML = `
            <div class="certificate-info">
                <h4>${cert.student_name}</h4>
                <p>${cert.filename}</p>
            </div>
            <div class="certificate-actions">
                <button class="btn btn-secondary" onclick="previewCertificate(${index})">Preview</button>
                <button class="btn btn-secondary" onclick="downloadCertificate(${index})">Download</button>
            </div>
        `;
        certificateList.appendChild(certDiv);
    });
}

// Preview certificate
function previewCertificate(index) {
    window.open(`/preview/${index}`, '_blank');
}

// Download certificate
function downloadCertificate(index) {
    window.location.href = `/download/${index}`;
}

// Send emails
async function sendEmails() {
    const customMessage = document.getElementById('email-message').value;
    
    if (!confirm('Are you sure you want to send certificates to all students with email addresses?')) {
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch('/send_emails', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: customMessage
            })
        });
        
        const data = await response.json();
        
        hideLoading();
        
        if (response.ok) {
            showMessage('Email sending completed!', 'success');
            displayEmailResults(data.results);
        } else {
            showMessage(data.error || 'Email sending failed', 'error');
        }
    } catch (error) {
        hideLoading();
        showMessage('Error sending emails: ' + error.message, 'error');
    }
}

// Display email sending results
function displayEmailResults(results) {
    let successCount = 0;
    let failCount = 0;
    let noEmailCount = 0;
    
    results.forEach(result => {
        if (result.status === 'sent') successCount++;
        else if (result.status === 'failed') failCount++;
        else if (result.status === 'no_email') noEmailCount++;
    });
    
    let message = `Email Results:\n`;
    message += `✓ Sent: ${successCount}\n`;
    if (failCount > 0) message += `✗ Failed: ${failCount}\n`;
    if (noEmailCount > 0) message += `⚠ No email: ${noEmailCount}`;
    
    alert(message);
}

// Show loading spinner
function showLoading() {
    loading.classList.remove('hidden');
}

// Hide loading spinner
function hideLoading() {
    loading.classList.add('hidden');
}

// Show message
function showMessage(text, type = 'info') {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    messageDiv.textContent = text;
    
    messageContainer.appendChild(messageDiv);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        messageDiv.remove();
    }, 5000);
}
