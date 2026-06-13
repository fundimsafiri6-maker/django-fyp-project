import os, sys, json
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_complaints_system.settings')
sys.path.insert(0, os.path.dirname(__file__))
import django
django.setup()

from complaints.classifier import classify_complaint, get_classifier
import time

print("Loading model...", flush=True)
t0 = time.time()
model, vec = get_classifier()
print(f"Model loaded in {time.time()-t0:.2f}s", flush=True)

test_cases = [
    "My lecturer Dr. John has not submitted our exam results from last semester. I have asked him multiple times but he keeps ignoring me. This is affecting my GPA calculation.",
    "The assignment deadline for the database course was changed without notice. The module coordinator didn't inform us and now we are being penalized for late submission.",
    "The student portal keeps logging me out when I try to register for courses. I have tried using Chrome and Firefox but the same problem occurs.",
    "The wifi network in the library has been down for three days. I cannot access the online learning management system to download course materials.",
    "The water tap in the male hostel bathroom has been leaking for a week. The floor is always wet and it's becoming a safety hazard.",
    "The food in the cafeteria is very expensive and the portions are small. We are spending too much money on meals that are not even tasty.",
]

titles = [
    "Exam results not submitted",
    "Assignment deadline changed without notice",
    "Student portal keeps logging me out",
    "Library wifi network down",
    "Leaking water tap in hostel bathroom",
    "Expensive cafeteria food",
]

print()
print("=" * 80)
print("COMPLAINT CLASSIFIER DIAGNOSTIC TEST")
print("=" * 80)

def fmt(r):
    cat = r.get('category', '?')
    conf = r.get('confidence', r.get('ml_confidence', 0))
    return f"{cat:<10} {float(conf):.3f}  {r.get('reason','')[:80]}"

for i, desc in enumerate(test_cases):
    title = titles[i]
    expected = ["Academic", "Academic", "ICT", "ICT", "Other", "Other"][i]
    print(f"\n{'='*60}")
    print(f"TEST {i+1}: {title}")
    print(f"EXPECTED: {expected}")
    print(f"{'-'*60}")

    r_desc = classify_complaint(desc, model, vec)
    r_td  = classify_complaint(f"{title} {desc}", model, vec)
    r_dt  = classify_complaint(f"{desc} {title}", model, vec)

    print(f"  DESC ONLY    : {fmt(r_desc)}")
    print(f"  TITLE+DESC   : {fmt(r_td)}")
    print(f"  DESC+TITLE   : {fmt(r_dt)}")

print("\n" + "=" * 80)
print("DONE")
print("=" * 80)
