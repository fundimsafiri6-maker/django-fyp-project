"""
Test script for email notification functionality
This script tests the email notification system for complaint resolution
"""
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'comp_project.settings')
django.setup()

from complaints.models import Complaint, ComplaintResponse
from complaints.email_utils import send_complaint_resolution_email
from accounts.models import User
from django.core.mail import send_mail
from django.conf import settings

def test_email_configuration():
    """Test if email configuration is properly set"""
    print("Testing email configuration...")
    print(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
    print(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
    print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
    print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
    print("✓ Email configuration loaded successfully\n")

def test_email_sending():
    """Test if email can be sent"""
    print("Testing email sending...")
    try:
        send_mail(
            subject='Test Email from Complaints System',
            message='This is a test email to verify email configuration is working.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.EMAIL_HOST_USER],
            fail_silently=False,
        )
        print("✓ Test email sent successfully\n")
        return True
    except Exception as e:
        print(f"✗ Failed to send test email: {str(e)}\n")
        return False

def test_complaint_resolution_email():
    """Test complaint resolution email with a sample complaint"""
    print("Testing complaint resolution email...")
    
    # Get a sample complaint
    try:
        complaint = Complaint.objects.first()
        if not complaint:
            print("✗ No complaints found in database. Create a test complaint first.\n")
            return False
        
        print(f"Using complaint: {complaint.title} (ID: {complaint.id})")
        print(f"User: {complaint.user.username}")
        print(f"User email: {complaint.user.email}")
        print(f"Email verified: {complaint.user.is_email_verified}")
        
        # Test sending the email
        result = send_complaint_resolution_email(
            complaint=complaint,
            response_text="This is a test response from the system."
        )
        
        if result:
            print("✓ Complaint resolution email sent successfully\n")
        else:
            print("✗ Failed to send complaint resolution email\n")
        
        return result
        
    except Exception as e:
        print(f"✗ Error testing complaint resolution email: {str(e)}\n")
        return False

def main():
    print("=" * 60)
    print("Email Notification System Test")
    print("=" * 60 + "\n")
    
    # Test 1: Email configuration
    test_email_configuration()
    
    # Test 2: Email sending
    email_sent = test_email_sending()
    
    # Test 3: Complaint resolution email
    if email_sent:
        test_complaint_resolution_email()
    else:
        print("Skipping complaint resolution email test due to email sending failure\n")
    
    print("=" * 60)
    print("Test completed")
    print("=" * 60)

if __name__ == '__main__':
    main()
