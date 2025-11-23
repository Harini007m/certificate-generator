#!/usr/bin/env python3
"""
Simple test script to verify the certificate generator system components.
"""

import os
import sys
from utils.file_parser import FileParser
from utils.email_sender import EmailSender

def test_file_parser():
    """Test file parser with sample CSV."""
    print("Testing File Parser...")
    parser = FileParser()
    
    # Test CSV parsing
    csv_file = 'examples/sample_students.csv'
    if not os.path.exists(csv_file):
        print(f"❌ Sample file not found: {csv_file}")
        return False
    
    try:
        students = parser.parse_file(csv_file)
        if len(students) == 0:
            print("❌ No students parsed from CSV")
            return False
        
        print(f"✓ Successfully parsed {len(students)} students from CSV")
        
        # Check required fields
        for student in students:
            if 'name' not in student or not student['name']:
                print("❌ Student missing required 'name' field")
                return False
        
        print("✓ All students have required fields")
        return True
    except Exception as e:
        print(f"❌ File parser error: {e}")
        return False

def test_email_sender():
    """Test email sender initialization."""
    print("\nTesting Email Sender...")
    try:
        sender = EmailSender()
        print("✓ Email sender initialized successfully")
        
        if sender.simulation_mode:
            print("✓ Running in simulation mode (expected without credentials)")
        else:
            print("✓ Running with actual email credentials")
        
        return True
    except Exception as e:
        print(f"❌ Email sender error: {e}")
        return False

def test_imports():
    """Test that all required packages are importable."""
    print("\nTesting Imports...")
    required_packages = [
        ('flask', 'Flask'),
        ('PIL', 'Pillow'),
        ('pandas', 'pandas'),
        ('openpyxl', 'openpyxl'),
        ('docx', 'python-docx'),
        ('reportlab.pdfgen', 'reportlab'),
        ('PyPDF2', 'PyPDF2'),
    ]
    
    all_success = True
    for module, package in required_packages:
        try:
            __import__(module)
            print(f"✓ {package} imported successfully")
        except ImportError:
            print(f"❌ Failed to import {package}")
            all_success = False
    
    return all_success

def test_directories():
    """Test that necessary directories can be created."""
    print("\nTesting Directory Structure...")
    dirs = ['uploads', 'generated_certificates']
    
    all_success = True
    for dir_name in dirs:
        try:
            os.makedirs(dir_name, exist_ok=True)
            if os.path.exists(dir_name) and os.path.isdir(dir_name):
                print(f"✓ Directory '{dir_name}' exists or created")
            else:
                print(f"❌ Failed to create directory '{dir_name}'")
                all_success = False
        except Exception as e:
            print(f"❌ Directory error for '{dir_name}': {e}")
            all_success = False
    
    return all_success

def main():
    """Run all tests."""
    print("=" * 60)
    print("Certificate Generator System Tests")
    print("=" * 60)
    
    results = {
        'Imports': test_imports(),
        'Directories': test_directories(),
        'File Parser': test_file_parser(),
        'Email Sender': test_email_sender(),
    }
    
    print("\n" + "=" * 60)
    print("Test Results Summary")
    print("=" * 60)
    
    for test_name, result in results.items():
        status = "✓ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    all_passed = all(results.values())
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ All tests passed!")
        return 0
    else:
        print("❌ Some tests failed!")
        return 1

if __name__ == '__main__':
    sys.exit(main())
