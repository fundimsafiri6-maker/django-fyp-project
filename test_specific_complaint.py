"""
Test specific complaint: 'mr juma is biased in marks distribution'
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_complaints_system.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from complaints.ai_classifier import ComplaintClassifier

# Test the specific complaint
class MockComplaint:
    def __init__(self, title, description, category=''):
        self.title = title
        self.description = description
        self.category = category

complaint = MockComplaint('mr juma is biased in marks distribution', 'mr juma is biased in marks distribution')

print("Testing: 'mr juma is biased in marks distribution'")
print("=" * 60)

result = ComplaintClassifier.classify_complaint(complaint)

print(f"Department: {result['department']}")
print(f"Method: {result['method']}")
print(f"Reason: {result['reason']}")
print(f"Priority: {result['priority']}")
print(f"Confidence: {result['confidence_score']}")

print("\n" + "=" * 60)
if result['department'] == 'hod':
    print("✓ CORRECT: Classified as HOD")
else:
    print(f"✗ WRONG: Classified as {result['department']} instead of HOD")
