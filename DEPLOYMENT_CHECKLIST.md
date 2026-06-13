# 📋 Implementation Checklist & Deployment Guide

## Pre-Deployment Verification

### Code Changes Verification
- [x] `accounts/views.py` - register_view() rewritten with validation
- [x] `accounts/views.py` - delete_user() rewritten with atomic transaction
- [x] `accounts/views.py` - edit_user() enhanced with validation
- [x] `accounts/views.py` - Added imports (transaction, IntegrityError, logging)
- [x] `templates/accounts/register.html` - Updated with new form fields
- [x] `templates/accounts/register.html` - Enhanced JavaScript validation
- [x] `accounts/tests.py` - Added 25+ comprehensive test cases

### Database Considerations
- ℹ️ No migrations needed - all changes use existing fields
- ℹ️ Email field values not auto-converted to lowercase (done at input)
- ℹ️ Old uppercase emails will still exist but new duplicates prevented

### Configuration Check
```bash
✅ EMAIL_HOST configured
✅ EMAIL_HOST_USER configured  
✅ EMAIL_HOST_PASSWORD configured
✅ DEFAULT_FROM_EMAIL configured
```

### Django System Checks
```bash
python manage.py check
# Expected: System check identified no issues (0 silenced)
```

---

## Testing Steps

### Step 1: Run Unit Tests
```bash
# Run all tests
python manage.py test accounts

# Run specific test class
python manage.py test accounts.tests.UserRegistrationTestCase
python manage.py test accounts.tests.UserDeletionTestCase
python manage.py test accounts.tests.UserEditTestCase

# Run with verbose output
python manage.py test accounts -v 2
```

### Step 2: Manual Testing - Registration

#### Test 2.1: Valid Student Registration
1. Go to `/accounts/register/`
2. Fill form:
   - Username: `test_student_001`
   - Email: `test.student@example.com`
   - Password: `TestPass123`
   - Confirm: `TestPass123`
   - Role: Student
3. Click "Create Account"
4. ✅ Should redirect to login
5. ✅ Check email for verification link
6. ✅ Verify email works
7. ✅ Can now login

#### Test 2.2: Valid Staff Registration
1. Go to `/accounts/register/`
2. Fill form:
   - Username: `test_staff_001`
   - Email: `test.staff@example.com`
   - Password: `TestPass123`
   - Confirm: `TestPass123`
   - Role: Staff Member
   - Department: Academic
   - Registration Number: `STAFF001`
3. Click "Create Account"
4. ✅ Should redirect to login
5. ✅ Can login immediately (no email verification needed)
6. ✅ User has department assigned

#### Test 2.3: Password Validation
Try these passwords (all should fail):
- `pass` ❌ (too short)
- `password` ❌ (no uppercase, no number)
- `Pass` ❌ (too short)
- `Pass123` ❌ (only 7 chars)
- `PASS123` ❌ (no lowercase)
- `pass123` ❌ (no uppercase)

Try this password (should pass):
- `SecurePass123` ✅

#### Test 2.4: Email Case Insensitivity
1. Register user with `john@example.com`
2. Try to register another user with `JOHN@EXAMPLE.COM`
3. ✅ Should show "Email already registered" error
4. ✅ Second user should NOT be created

#### Test 2.5: Password Confirmation Mismatch
1. Fill registration form
2. Password: `TestPass123`
3. Confirm Password: `DifferentPass123`
4. ✅ Client-side error on blur
5. ✅ Server-side error if submitted

#### Test 2.6: Department Requirement
1. Select "Staff Member" role
2. Notice Department field appears
3. Leave department empty
4. Try to submit
5. ✅ JavaScript alert: "Department is required"
6. ✅ Server also validates (for direct form submission)

### Step 3: Manual Testing - User Deletion

#### Test 3.1: Delete User with Complaints
1. Login as admin
2. Go to User Management (`/accounts/admin-users/`)
3. Create a student with a complaint
4. Delete the student
5. ✅ No system crash
6. ✅ "User successfully deleted" message
7. ✅ Complaint is also deleted (cascade)
8. ✅ Check logs show "Deleting X complaints"

#### Test 3.2: Delete Staff with Assigned Complaints
1. Create staff member (e.g., `staff_test`)
2. Assign complaints to staff
3. Go to admin users
4. Delete staff member
5. ✅ No crash
6. ✅ Complaints still exist but `assigned_to = NULL`
7. ✅ Complaints show as "Unassigned"

#### Test 3.3: Prevent Self-Deletion
1. Login as admin
2. Go to admin users
3. Find self in list
4. Click delete button
5. ✅ Error: "You cannot delete your own account!"
6. ✅ Admin account still exists

### Step 4: Manual Testing - User Edit

#### Test 4.1: Email Edit with Case Insensitivity
1. Admin user exists with `john@example.com`
2. Edit another user
3. Try to change their email to `JOHN@EXAMPLE.COM`
4. ✅ Error: "Email is already in use by another user"
5. ✅ Changes not saved

#### Test 4.2: Promote Student to Staff
1. Create student user
2. Edit that user
3. Change Role to "Staff Member"
4. Notice Department field now required
5. Leave Department empty
6. Try to submit
7. ✅ Error: "Department is required for staff users"

#### Test 4.3: Successful Role Promotion
1. Create student
2. Edit to Staff with department=Academic
3. Save
4. ✅ User now has role='staff'
5. ✅ User has department='academic'
6. ✅ User is active immediately

---

## Environment Setup

### Required Environment Variables
```
# Email Configuration (REQUIRED for registration)
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-specific-password
DEFAULT_FROM_EMAIL=noreply@system.com

# Database (should already be set)
DB_NAME=your_database_name
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306

# Django Settings
SECRET_KEY=your-secret-key
DEBUG=False  # Set to False in production
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Create Admin User (if needed)
```bash
python manage.py createsuperuser
# Follow prompts to create admin account
```

---

## Verification Checklist

### After Deployment

- [ ] Run `python manage.py check` - no errors
- [ ] Run `python manage.py test accounts` - all tests pass
- [ ] Test student registration with email verification
- [ ] Test staff registration with department requirement
- [ ] Test user deletion without system crash
- [ ] Verify email sending works for new students
- [ ] Check Django admin still works
- [ ] Monitor error logs for first hour
- [ ] Test role changes preserve/set department correctly
- [ ] Verify case-insensitive email checking works

### Performance Verification
- [ ] Registration takes <100ms
- [ ] User deletion takes <500ms
- [ ] Email sending takes <2s
- [ ] No database query N+1 issues

### Security Verification
- [x] Passwords validated for strength
- [x] Email case-insensitive preventing duplicates
- [x] SQL injection prevention (ORM used)
- [x] CSRF protection (Django default)
- [x] Session security (Django default)

---

## Rollback Plan

If issues occur post-deployment:

### Option 1: Revert Code Changes
```bash
git revert <commit-hash>
python manage.py runserver
# Test to confirm rollback works
```

### Option 2: Database Repair
If database has orphaned records:
```python
# In Django shell
python manage.py shell

# Find orphaned complaints (assigned_to user that doesn't exist)
from complaints.models import Complaint
orphaned = Complaint.objects.filter(assigned_to__isnull=False)
# Check if user still exists

# If needed, clean up
orphaned.update(assigned_to=None)
```

---

## Monitoring After Deployment

### Log Files to Watch
```
- Django error logs (500 errors)
- Database transaction logs
- Email sending logs (in /var/log/mail)
```

### Error Messages to Watch For
- "FOREIGN KEY constraint failed" - cascade handling issue
- "Email already registered" - email normalization issue  
- "Department is required" - validation working correctly
- "Transaction rolled back" - atomic transaction issue

### Metrics to Track
- Registration success rate
- User deletion success rate
- Email sending success rate
- Average response times

---

## Known Issues & Workarounds

### Issue 1: Email Verification Not Sending
**Symptoms:** Students can't verify email
**Check:**
```python
# In Django shell
from django.core.mail import send_mail
send_mail('Test', 'Body', 'from@example.com', ['to@example.com'])
```
**Fix:** Check EMAIL_* settings in `.env`

### Issue 2: Old Uppercase Emails
**Symptoms:** Case-insensitive check fails for existing data
**Cause:** Old emails not normalized during deployment
**Fix:**
```python
# Run once in Django shell
from accounts.models import User
for user in User.objects.all():
    user.email = user.email.lower()
    user.save()
```

### Issue 3: Department Field Missing
**Symptoms:** Staff users created without department
**Fix:**
```python
# Check and fill missing departments
from accounts.models import User
User.objects.filter(role='staff', department__isnull=True).update(department='other')
```

---

## Support & Documentation

- **Validation Requirements:** See `VALIDATION_REQUIREMENTS.md`
- **Bug Fixes Summary:** See `BUG_FIXES_SUMMARY.md`  
- **Previous Fixes:** See `fixes-may-2026.md`
- **Test Coverage:** See `accounts/tests.py`

---

## Rollout Timeline

| Phase | Duration | Action |
|-------|----------|--------|
| 1. Testing | 1-2 hours | Run full test suite locally |
| 2. Staging | 1-2 hours | Deploy to staging, run tests |
| 3. Production | 30 min | Deploy to production |
| 4. Monitoring | 1 hour | Watch error logs closely |
| 5. Validation | 2-4 hours | Manual testing on production |

---

**Deployment Date:** [To be filled]
**Deployed By:** [To be filled]
**Status:** ⏳ Ready for Deployment