import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sms_service import send_sms

send_sms(
    "255763394096",
    "Test SMS from AI Complaint System"
)