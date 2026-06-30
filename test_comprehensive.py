import sys
sys.path.insert(0, '.')
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_complaints_system.settings')
django.setup()
from complaints.classifier import classify_complaint

tests = [
    # Academic
    ('i need to understand programming', 'Academic'),
    ('i am having trouble with coding assignments', 'Academic'),
    ('the course material is not accessible on the portal', 'Academic'),
    ('i need help with data structures', 'Academic'),
    ('i need tutoring for my programming course', 'Academic'),
    ('the lecture notes are not accessible online', 'Academic'),
    ('my marks have been entered incorrectly in the portal', 'Academic'),
    ('i am struggling with the python programming exercises', 'Academic'),
    # ICT
    ('the wifi is not working in the hostel', 'ICT'),
    ('i cannot login to the student portal', 'ICT'),
    ('system not allowing course registration', 'ICT'),
    ('the email system is down', 'ICT'),
    ('the network is very slow today', 'ICT'),
    # Other
    ('the bathroom is dirty and needs cleaning', 'Other'),
    ('i want to go home', 'Other'),
    ('the air conditioner is not working', 'Other'),
    ('the food in the cafeteria is cold', 'Other'),
    ('there is no water in the hostel', 'Other'),
    # HOD
    ('my lecturer is harassing me', 'HOD'),
    ('the lecturer is seducing girls in class', 'HOD'),
]

all_pass = True
for text, expected in tests:
    result = classify_complaint(text)
    cat = result['category']
    if cat != expected:
        all_pass = False
        print(f'FAIL: "{text[:60]}" -> {cat} (expected {expected})')

print('ALL PASS' if all_pass else 'SOME FAILED')
