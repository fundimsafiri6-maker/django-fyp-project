#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_complaints_system.settings')
django.setup()

from accounts.models import User
from complaints.models import Complaint, ComplaintResponse

# Get testuser
try:
    user = User.objects.get(username='testuser')
    print(f"Found user: {user.username} (ID: {user.id})")
    
    # Check related objects
    complaints = Complaint.objects.filter(user=user)
    print(f"Complaints by user: {complaints.count()}")
    
    responses = ComplaintResponse.objects.filter(staff_member=user)
    print(f"Responses by user: {responses.count()}")
    
    assigned = Complaint.objects.filter(assigned_to=user)
    print(f"Complaints assigned to user: {assigned.count()}")
    
    # Now try to delete
    print("\nDeleting user...")
    user.delete()
    print("✅ User deleted successfully!")
    
    # Verify deletion
    try:
        User.objects.get(username='testuser')
        print("❌ User still exists - deletion failed!")
    except User.DoesNotExist:
        print("✅ User no longer exists - deletion confirmed!")
        
except User.DoesNotExist:
    print("❌ User 'testuser' not found")
except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()
