# Department-Specific Staff Dashboards with AI Complaint Routing

## Overview
A complete department-based complaint management system where the AI model automatically classifies and routes complaints to specific departments. Each department (Academic, ICT, Administration, Student Affairs) has its own specialized dashboard showing only relevant complaints.

## What's Been Implemented

### 1. **AI Complaint Classifier** (`complaints/ai_classifier.py`)
A flexible classification system that:
- Classifies complaints into departments using keyword matching (rule-based, ready for ML model integration)
- Assesses complaint priority (Urgent, High, Medium, Low)
- Routes complaints to available staff members in the department
- Calculates AI confidence scores (0-100%)

**Key Classes:**
- `ComplaintClassifier`: Handles classification logic
- `DepartmentRouter`: Routes complaints to departments and staff

### 2. **Updated Complaint Model**
New fields added to support automatic routing:
- `department`: CharField with choices (academic, ict, other)
- `ai_confidence_score`: Float field (0-100) showing AI classification confidence
- `ai_classified`: Boolean flag indicating if complaint was AI-processed

### 3. **Department-Specific Staff Dashboards**

Each department has its own dashboard accessible at:
 - **Academic**: `/accounts/academic-dashboard/` - Shows academic-related complaints
 - **ICT**: `/accounts/ict-dashboard/` - Shows technology/system complaints
 - **Other**: `/accounts/staff-dashboard/` - Shows other/general complaints (handled by admin)

**Dashboard Features:**
- Department-specific complaint statistics (pending, in progress, resolved, urgent)
- Real-time charts (Status and Priority distributions)
- Quick access to urgent cases
- Unassigned complaint queue
- Staff team member list
- AI classification confidence tracking

### 4. **Automatic Complaint Routing**
When a student submits a complaint:
1. AI classifier analyzes the text
2. Determines most likely department based on keywords
3. Assigns appropriate priority level
4. Automatically assigns to least-busy staff member in that department
5. Stores confidence score for transparency

### 5. **Department-Based Staff Access Control**
- Staff members only see complaints in their assigned department
- Admin users can see all complaints and switch between departments
- Department filtering throughout the system

## How to Set Up

### Step 1: Run Database Migration
```bash
python manage.py migrate
```

This will:
- Add `department`, `ai_confidence_score`, `ai_classified` fields to Complaint model
- Remove old `department_id` field

### Step 2: Assign Staff to Departments
You need to manually assign staff members to departments in Django Admin or using the admin panel:

1. Go to Admin Users page (`/accounts/admin-users/`)
2. Edit each staff member
3. Set their `department` field to: academic, ict, or other

### Step 3: Test the System

**Create Test Data:**
```bash
python manage.py shell

from accounts.models import User
from complaints.models import Complaint

# Create test staff members
staff1 = User.objects.create_user(
    username='academic_staff', 
    password='test123', 
    role='staff', 
    department='academic'
)

staff2 = User.objects.create_user(
    username='ict_staff', 
    password='test123', 
    role='staff', 
    department='ict'
)

# Test complaint submission (this will auto-classify and route)
# Submit through the web interface or use the shell
complaint = Complaint.objects.create(
    title='Cannot access online registration system',
    description='The SR2 portal keeps timing out when trying to register courses',
    category='Technology Issue',
    user=User.objects.filter(role='student').first(),
    priority='High'
)

# Check if AI processed it
print(f"Department: {complaint.department}")
print(f"Assigned to: {complaint.assigned_to}")
print(f"Confidence: {complaint.ai_confidence_score}%")
```

### Step 4: Access Department Dashboards
Staff members will:
1. Log in as staff with a department assigned
2. Be redirected to `/accounts/staff-dashboard/` (generic view)
3. Can access their department-specific dashboard
4. See only complaints for their department

## Integration with Your ML Model

The system is designed to be easily integrated with your custom ML model.

### Current Implementation (Rule-based)
Located in `complaints/ai_classifier.py`, using keyword matching for classification.

### To Replace with Your ML Model:

**Option 1: Override the classifier class**
```python
from complaints.ai_classifier import ComplaintClassifier

class YourMLClassifier(ComplaintClassifier):
    @classmethod
    def _classify_department(cls, text):
        # Call your ML model
        model = load_your_model()
        prediction = model.predict(text)
        return prediction['department'], prediction['confidence']
    
    @classmethod
    def _assess_priority(cls, text):
        # Call your priority model
        priority_model = load_priority_model()
        return priority_model.predict(text)
```

**Option 2: Modify the submit_complaint view**
```python
from your_ml_module import classify_and_route

@student_required
def submit_complaint(request):
    if request.method == 'POST':
        # Create complaint
        complaint = Complaint.objects.create(...)
        
        # Use your ML model
        result = classify_and_route(complaint)
        complaint.department = result['department']
        complaint.ai_confidence_score = result['confidence']
        complaint.save()
```

## File Structure

```
complaints/
├── ai_classifier.py          # Classification and routing engine
├── models.py                 # Updated Complaint model
├── views.py                  # Updated with AI processing
├── urls.py                   # Complaint URLs
└── migrations/
    └── 0003_complaint_department_fields.py   # New migration

accounts/
├── views.py                  # NEW: Department dashboards
├── urls.py                   # NEW: Department dashboard URLs
└── models.py                 # User model (already has department field)

templates/dashboard/
├── academic_dashboard.html   # Academic department dashboard
├── ict_dashboard.html        # ICT department dashboard
└── staff_dashboard.html      # Other/general department dashboard
```

## API Reference

### ComplaintClassifier

```python
# Classify a complaint
result = ComplaintClassifier.classify_complaint(complaint)
# Returns: {
#     'department': 'academic',
#     'confidence_score': 85.5,
#     'priority': 'High'
# }

# Full processing (classify + update complaint)
complaint = ComplaintClassifier.process_complaint(complaint)
# Updates: department, priority, ai_confidence_score, ai_classified
```

### DepartmentRouter

```python
# Assign complaint to available staff in department
complaint = DepartmentRouter.assign_to_staff(complaint)

# Or manually assign to specific staff
complaint = DepartmentRouter.assign_to_staff(complaint, staff_member=user)

# Get department staff
staff = DepartmentRouter.get_department_staff('academic')

# Get department complaints
complaints = DepartmentRouter.get_department_complaints('ict')
```

## Department Classification Keywords

The system uses keyword matching for default classification:

- **Academic**: course, exam, grade, lecture, assignment, registration, tuition, etc.
- **ICT**: internet, network, computer, email, password, login, website, portal, etc.
- **Other**: administration, finance, payment, welfare, health, safety, general inquiries, etc.

Customize these keywords in `complaints/ai_classifier.py` → `DEPARTMENT_KEYWORDS` dict.

## Testing Checklist

- [ ] Run migration: `python manage.py migrate`
- [ ] Create test staff in each department
- [ ] Submit a test complaint and verify:
  - [ ] Department field is populated
  - [ ] Complaint appears in correct department dashboard
  - [ ] Staff member in that department can see it
  - [ ] AI confidence score is calculated
- [ ] Test department dashboard access:
  - [ ] Academic staff sees `/accounts/academic-dashboard/`
  - [ ] ICT staff sees `/accounts/ict-dashboard/`
  - [ ] Other dashboards work similarly
- [ ] Test unassigned complaint queue
- [ ] Test urgent complaint highlighting
- [ ] Verify charts render correctly
- [ ] Test staff assignment workflow

## Troubleshooting

**Problem**: Staff can't see their department dashboard
- **Solution**: Ensure staff member has their `department` field set in User model

**Problem**: Complaints not routing to correct department
- **Solution**: Check `ai_classifier.py` keywords or manually test classification:
  ```python
  from complaints.ai_classifier import ComplaintClassifier
  result = ComplaintClassifier.classify_complaint(complaint)
  print(result)
  ```

**Problem**: Staff dashboard appears empty
- **Solution**: 
  - Verify complaints exist in the database
  - Check if staff member's department matches complaint's department
  - Look at database directly: `Complaint.objects.filter(department='academic')`

**Problem**: Migration fails
- **Solution**: 
  - Check if any complaints exist: `Complaint.objects.count()`
  - Delete conflicting migrations if corrupted
  - Run `python manage.py makemigrations` again

## Future Enhancements

1. **Real ML Model Integration**: Replace keyword matching with your trained model
2. **Manual Override**: Allow staff to recategorize complaints
3. **Department Reassignment**: Let admins move complaints between departments
4. **Bulk Operations**: Assign multiple complaints at once
5. **SLA Tracking**: Track resolution time by department
6. **Department Reports**: Generate department-specific reports
7. **Predictive Routing**: Use ML to predict best staff member (not just least busy)
8. **Quality Scoring**: Track misclassification rates and model performance
9. **Auto-escalation**: Escalate urgent cases automatically
10. **Integration with Email/SMS**: Notify staff of new complaints in their queue

## Support

For questions about:
- **AI Integration**: Reference `complaints/ai_classifier.py`
- **Views & URLs**: Check `accounts/views.py` and `accounts/urls.py`
- **Styling**: Department dashboards in `templates/dashboard/*.html`
- **Database**: See migrations in `complaints/migrations/`
