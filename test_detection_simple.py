"""
Simple test of detection logic without Django setup
"""
import sys
sys.path.insert(0, r'C:\Users\AUDITORIUM\Pictures\comp_project')

from complaints.improved_classifier_django import OutOfDepartmentDetector

# Test cases
test_cases = [
    "i need a wife",
    "need a husband",
    "want to marry",
    "looking for girlfriend",
    "assignment deadline unclear",  # Should NOT be out-of-department
    "lecturer juma is corrupt",  # Should NOT be out-of-department (HOD)
]

print("=" * 80)
print("TESTING DETECTION WITHOUT DJANGO SETUP")
print("=" * 80)

detector = OutOfDepartmentDetector()

for text in test_cases:
    is_ood, reason = detector.is_out_of_department(text)
    print(f"\nText: '{text}'")
    print(f"  Is Out-of-Department: {is_ood}")
    print(f"  Reason: {reason}")

print("\n" + "=" * 80)
print("TEST COMPLETE")
print("=" * 80)
