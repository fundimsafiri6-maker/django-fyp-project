"""
Test Django integration with wife/romance detection fix
"""
import sys
import os
sys.path.insert(0, r'C:\Users\AUDITORIUM\Pictures\comp_project')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_complaints_system.settings')

import django
django.setup()

from complaints.ai_classifier import ComplaintClassifier

# Test cases
test_cases = [
    "i need a wife",
    "need a husband",
    "want to marry",
    "looking for girlfriend",
    "assignment deadline unclear",  # Should be Academic
    "lecturer juma is corrupt",  # Should be HOD
]

print("=" * 80)
print("TESTING DJANGO INTEGRATION WITH WIFE/ROMANCE FIX")
print("=" * 80)

for text in test_cases:
    print(f"\nTesting: '{text}'")
    
    # Create a mock complaint object
    class MockComplaint:
        def __init__(self, text):
            self.title = text
            self.description = text
            self.category = ""
    
    complaint = MockComplaint(text)
    
    try:
        result = ComplaintClassifier.classify_complaint(complaint)
        print(f"  Department: {result['department']}")
        print(f"  Priority: {result['priority']}")
        print(f"  Reason: {result['reason']}")
        print(f"  Method: {result['method']}")
    except Exception as e:
        print(f"  ERROR: {str(e)}")

print("\n" + "=" * 80)
print("TEST COMPLETE")
print("=" * 80)
