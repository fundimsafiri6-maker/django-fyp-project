"""
Test script to verify the Django classifier correctly handles 'Other' category
"""

import os
import sys
import django

# Setup Django
sys.path.append(r'C:\Users\AUDITORIUM\Pictures\comp_project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_complaints_system.settings')
django.setup()

from complaints.ai_classifier import ComplaintClassifier

print("=" * 100)
print("TESTING DJANGO CLASSIFIER - 'Other' Category Handling")
print("=" * 100)

# Test cases that should be classified as 'Other' (not ICT, not ACADEMIC, not HOD)
test_cases = [
    ("The bathroom is dirty", "other"),
    ("The food in the cafeteria is cold", "other"),
    ("There is no water in the hostel", "other"),
    ("The parking lot is full", "other"),
    ("The air conditioner is not working", "other"),
    ("I need a refund for my hostel fees", "other"),
    ("The security guard is rude", "other"),
    ("My room has a broken window", "other"),
    ("The bus is always late", "other"),
    ("I need to get my student ID card replaced", "other"),
]

# Test cases that should NOT be 'other'
negative_test_cases = [
    ("The system is down", "ict"),
    ("My login credentials are not recognized", "ict"),
    ("Assignment deadline was not clearly communicated", "academic"),
    ("The lecturer has not uploaded course materials", "academic"),
]

print("\n" + "=" * 100)
print("POSITIVE TESTS: Should be classified as 'other'")
print("=" * 100)

passed = 0
failed = 0

for title, expected_dept in test_cases:
    # Create a mock complaint object
    class MockComplaint:
        def __init__(self, title, description=""):
            self.title = title
            self.description = description
            self.category = ""
            self.department = ""
            self.priority = ""
            self.ai_confidence_score = 0.0
            self.ai_classified = False
    
    complaint = MockComplaint(title)
    
    try:
        result = ComplaintClassifier.classify_complaint(complaint)
        predicted_dept = result['department']
        
        if predicted_dept == expected_dept:
            passed += 1
            status = "[PASS]"
        else:
            failed += 1
            status = "[FAIL]"
        
        print(f"\n{status}")
        print(f"  Complaint: {title}")
        print(f"  Expected: {expected_dept}")
        print(f"  Got: {predicted_dept}")
        print(f"  Reason: {result['reason']}")
        print(f"  Method: {result['method']}")
    except Exception as e:
        failed += 1
        print(f"\n[ERROR]")
        print(f"  Complaint: {title}")
        print(f"  Error: {str(e)}")

print("\n" + "=" * 100)
print(f"POSITIVE TESTS RESULTS: {passed}/{len(test_cases)} passed")
print("=" * 100)

print("\n" + "=" * 100)
print("NEGATIVE TESTS: Should NOT be classified as 'other'")
print("=" * 100)

neg_passed = 0
neg_failed = 0

for title, expected_dept in negative_test_cases:
    complaint = MockComplaint(title)
    
    try:
        result = ComplaintClassifier.classify_complaint(complaint)
        predicted_dept = result['department']
        
        if predicted_dept == expected_dept:
            neg_passed += 1
            status = "[PASS]"
        else:
            neg_failed += 1
            status = "[FAIL]"
        
        print(f"\n{status}")
        print(f"  Complaint: {title}")
        print(f"  Expected: {expected_dept}")
        print(f"  Got: {predicted_dept}")
        print(f"  Reason: {result['reason']}")
        print(f"  Method: {result['method']}")
    except Exception as e:
        neg_failed += 1
        print(f"\n[ERROR]")
        print(f"  Complaint: {title}")
        print(f"  Error: {str(e)}")

print("\n" + "=" * 100)
print(f"NEGATIVE TESTS RESULTS: {neg_passed}/{len(negative_test_cases)} passed")
print("=" * 100)

print("\n" + "=" * 100)
print(f"OVERALL RESULTS: {passed + neg_passed}/{len(test_cases) + len(negative_test_cases)} tests passed")
print("=" * 100)

if failed == 0 and neg_failed == 0:
    print("\n[SUCCESS] All tests passed! The Django classifier correctly handles 'Other' category")
else:
    print(f"\n[WARNING] {failed + neg_failed} tests failed. The classifier may need further adjustment.")
