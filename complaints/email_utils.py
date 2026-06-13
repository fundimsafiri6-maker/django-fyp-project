from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def send_complaint_resolution_email(complaint, response_text=None):
    """
    Send email notification to user when their complaint is resolved.
    Only sends if user has a verified email.
    
    Args:
        complaint: The Complaint object that was resolved
        response_text: Optional response text from staff/admin
    
    Returns:
        bool: True if email was sent successfully, False otherwise
    """
    user = complaint.user
    
    # Check if user has a verified email
    if not user.email:
        logger.warning(f"User {user.username} has no email address. Cannot send resolution notification for complaint {complaint.id}")
        return False
    
    if not user.is_email_verified:
        logger.warning(f"User {user.username} email is not verified. Cannot send resolution notification for complaint {complaint.id}")
        return False
    
    try:
        # Prepare email context
        context = {
            'user': user,
            'complaint': complaint,
            'response_text': response_text,
            'site_name': getattr(settings, 'SITE_NAME', 'UDOM Complaints System'),
        }
        
        # Render email templates
        subject = render_to_string('complaints/email/complaint_resolved_subject.txt', context).strip()
        message = render_to_string('complaints/email/complaint_resolved.txt', context)
        html_message = render_to_string('complaints/email/complaint_resolved.html', context)
        
        # Send email
        send_mail(
            subject=subject,
            message=message,
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@udom-complaints.ac.tz'),
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        logger.info(f"Successfully sent resolution email to {user.email} for complaint {complaint.id}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send resolution email to {user.email} for complaint {complaint.id}: {str(e)}")
        return False
