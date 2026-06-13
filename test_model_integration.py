"""
Test script to verify ML model integration fix
Tests that complaints like "mr baraka is biased" are correctly classified as HOD
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_complaints_system.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from complaints.ai_classifier import ComplaintClassifier
from complaints.models import Complaint

# Test cases
test_cases = [
    {
        'title': 'mr baraka is biased',
        'description': 'mr baraka is biased in his marking',
        'expected_department': 'hod',
        'description': 'Should be classified as HOD (staff complaint with name)'
    },
    {
        'title': 'lecturer unfair treatment',
        'description': 'the lecturer treats me unfairly',
        'expected_department': 'hod',
        'description': 'Should be classified as HOD (staff complaint)'
    },
    {
        'title': 'mr henry is very strict',
        'description': 'mr henry is very strict with students',
        'expected_department': 'hod',
        'description': 'Should be classified as HOD (staff complaint with name and behavior)'
    },
    {
        'title': 'wifi not working',
        'description': 'the wifi in the library is not working',
        'expected_department': 'ict',
        'description': 'Should be classified as ICT'
    },
    {
        'title': 'exam schedule',
        'description': 'when is the exam for CS101',
        'expected_department': 'academic',
        'description': 'Should be classified as Academic'
    },
    {
        'title': 'broken toilet',
        'description': 'the toilet in block A is broken',
        'expected_department': 'other',
        'description': 'Should be classified as Other (facilities)'
    }
]

print("Testing ML Model Integration Fix")
print("=" * 60)

passed = 0
failed = 0

for i, test in enumerate(test_cases, 1):
    print(f"\nTest {i}: {test['description']}")
    print(f"Input: '{test['title']}' - '{test['description']}'")
    
    # Create a mock complaint object
    class MockComplaint:
        def __init__(self, title, description, category=''):
            self.title = title
            self.description = description
            self.category = category
    
    complaint = MockComplaint(test['title'], test['description'])
    
    # Classify
    result = ComplaintClassifier.classify_complaint(complaint)
    
    actual_dept = result['department']
    expected_dept = test['expected_department']
    
    print(f"Expected: {expected_dept}")
    print(f"Actual: {actual_dept}")
    print(f"Method: {result['method']}")
    print(f"Reason: {result['reason']}")
    
    if actual_dept == expected_dept:
        print("✓ PASSED")
        passed += 1
    else:
        print("✗ FAILED")
        failed += 1

print("\n" + "=" * 60)
print(f"Results: {passed} passed, {failed} failed out of {len(test_cases)} tests")

if failed == 0:
    print("All tests passed! ✓")
else:
    print(f"{failed} test(s) failed. ✗")
