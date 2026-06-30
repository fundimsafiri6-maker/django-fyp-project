import os
import requests
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

AUTH = os.getenv("BULKSMS_AUTH")
SMS_ENABLED = os.getenv("SMS_ENABLED", "True").lower() in ("true", "1", "yes")


def send_sms(phone, message):
    if not AUTH:
        logger.warning("BULKSMS_AUTH not set. Skipping SMS send.")
        return None
    if not SMS_ENABLED:
        logger.info("SMS disabled via SMS_ENABLED env var. Would send to %s: %s", phone, message[:50])
        return None

    url = "https://api.bulksms.com/v1/messages"
    payload = {"to": phone, "body": message}
    headers = {"Authorization": AUTH, "Content-Type": "application/json"}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        logger.info("SMS to %s: HTTP %s", phone, response.status_code)
        return response.json()
    except Exception as e:
        logger.error("SMS send failed to %s: %s", phone, str(e))
        return None


def send_bulk_sms(phone_numbers, message):
    if not AUTH:
        logger.warning("BULKSMS_AUTH not set. Skipping bulk SMS.")
        return None
    if not SMS_ENABLED:
        logger.info("SMS disabled. Would send bulk to %d recipients: %s", len(phone_numbers), message[:50])
        return None

    url = "https://api.bulksms.com/v1/messages"
    payload = {"to": phone_numbers if len(phone_numbers) > 1 else phone_numbers[0], "body": message}
    headers = {"Authorization": AUTH, "Content-Type": "application/json"}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=15)
        logger.info("Bulk SMS to %d numbers: HTTP %s", len(phone_numbers), response.status_code)
        return response.json()
    except Exception as e:
        logger.error("Bulk SMS failed: %s", str(e))
        return None


def send_complaint_status_sms(complaint):
    user = complaint.user
    if not user.phone_number:
        logger.warning("User %s has no phone number. Cannot send SMS.", user.username)
        return False
    if complaint.status not in ("Resolved", "Rejected"):
        return False

    action = "resolved" if complaint.status == "Resolved" else "rejected"
    message = (
        f"Dear {user.username}, your complaint : {complaint.title} has been {action}."
          
    )
    try:
        send_sms(user.phone_number, message)
    except Exception as e:
        logger.error("Failed to send status SMS to %s: %s", user.phone_number, str(e))
    return True


def send_high_priority_bulk_sms(complaint):
    if complaint.priority not in ("Medium", "High"):
        return False
    if complaint.status not in ("Resolved", "Rejected"):
        return False

    from accounts.models import User
    staff_users = User.objects.filter(
        role__in=("staff", "admin", "hod"),
    ).exclude(phone_number__isnull=True).exclude(phone_number__exact="")
    phone_numbers = list(staff_users.values_list("phone_number", flat=True))
    if not phone_numbers:
        return False

    action = "resolved" if complaint.status == "Resolved" else "rejected"
    message = (
        f"HIGH PRIORITY complaint #{complaint.id} {action}: {complaint.title}. "
       
    )
    try:
        send_bulk_sms(phone_numbers, message)
    except Exception as e:
        logger.error("Failed to send high priority bulk SMS: %s", str(e))
    return True
