# Django Complaints System - Bug Analysis Report
**Date:** May 13, 2026  
**Project:** AI Complaints System  
**Scope:** User Registration, User Deletion, Data Integrity Analysis

---

## EXECUTIVE SUMMARY

Found **12 critical/high-priority bugs** related to:
- Missing field validations in user registration
- Data integrity issues with redundant fields
- Cascade delete problems when users are deleted
- Password and email validation gaps
- Transaction safety issues
- Orphaned data scenarios

---

## 1. USER REGISTRATION ISSUES

### BUG #1: Missing Password Validation
**File:** [accounts/views.py](accounts/views.py#L398)  
**Location:** `register_view()` function, lines 380-440  
**Severity:** HIGH

**Issue:** No password validation is performed before creating the user.
```python
# Line 398: Password directly passed to create_user without validation
user = User.objects.create_user(
    username=username,
    email=email,
    password=password,  # NO VALIDATION
    role=role,
    is_active=is_active
)
```

**Problems:**
- Passwords can be empty strings
- No minimum length requirement (Django default is 8 chars, but not enforced here)
- No complexity requirements (uppercase, lowercase, numbers, special chars)
- Users can register with single-character passwords

**Impact:** Weak passwords allow brute-force attacks and compromised accounts.

---

### BUG #2: Missing Email Validation
**File:** [accounts/views.py](accounts/views.py#L389)  
**Location:** `register_view()` function, line 389  
**Severity:** MEDIUM

**Issue:** Email format is never validated.
```python
# Lines 388-390: Only checks if email exists, not if it's valid format
if User.objects.filter(email=email).exists():
    messages.error(request, "Email already registered")
    return render(request, "accounts/register.html")
```

**Problems:**
- Invalid email formats accepted (e.g., "not-an-email", "@example", "user@")
- No domain validation
- Can store garbage data in email field

**Impact:** Users can create accounts with invalid emails, breaking email verification flow.

---

### BUG #3: No Password Confirmation Field
**File:** [accounts/views.py](accounts/views.py#L392)  
**Location:** `register_view()` function, line 392  
**Severity:** MEDIUM

**Issue:** Registration form only gets password once - no confirmation check.

**Problems:**
- Users cannot verify they typed password correctly
- Typos lock users out until password reset
- No client-side or server-side confirmation validation

**Impact:** Poor UX and account lockouts from typos.

---

### BUG #4: Missing Required Field Validation for Staff/Admin Roles
**File:** [accounts/views.py](accounts/views.py#L398)  
**Location:** `register_view()` function, line 398-408  
**Severity:** HIGH

**Issue:** Staff and admin users can be created without required department assignment.

```python
# Staff/Admin created without enforcing department field
user = User.objects.create_user(
    username=username,
    email=email,
    password=password,
    role=role,  # Can be 'staff' or 'admin' without department
    is_active=is_active
)
```

**Related Model Issue:** [accounts/models.py](accounts/models.py#L17-L20)
```python
department = models.CharField(
    max_length=100, blank=True, null=True  # Should be required for staff/admin
)
```

**Problems:**
- Staff users created without departments cannot properly filter complaints
- Breaks staff dashboard logic that assumes department is set
- Administrative oversight: cannot enforce organizational structure

**Impact:** Staff dashboard shows all complaints instead of department-specific ones.

---

### BUG #5: No Role Validation During Registration
**File:** [accounts/views.py](accounts/views.py#L393)  
**Location:** `register_view()` function, line 393  
**Severity:** MEDIUM

**Issue:** Role parameter not validated against ROLE_CHOICES.
```python
role = request.POST.get("role", "student")  # Can be any string!
```

**Problems:**
- Invalid roles accepted (e.g., "superuser", "moderator", "hacker")
- No check against defined ROLE_CHOICES
- Can bypass role-based access control

**Impact:** Users could create accounts with roles not defined in the system.

---

### BUG #6: Email Case Sensitivity Creates Duplicate Accounts
**File:** [accounts/views.py](accounts/views.py#L388-390)  
**Location:** `register_view()` function, lines 388-390  
**Severity:** MEDIUM

**Issue:** Email uniqueness check is case-sensitive.
```python
if User.objects.filter(email=email).exists():  # Case-sensitive
```

**Scenario:**
- User 1 registers with "user@example.com"
- User 2 registers with "USER@EXAMPLE.COM" - ALLOWED
- System treats them as different accounts

**Problems:**
- Duplicate email accounts in database
- Email verification sends to same inbox, confusing users
- Breaks email-based password recovery

**Impact:** Multiple accounts for same email address.

---

## 2. USER DELETION ISSUES

### BUG #7: Orphaned EmailVerificationToken Records After Failed Email Send
**File:** [accounts/views.py](accounts/views.py#L409-430)  
**Location:** `register_view()` function, lines 409-430  
**Severity:** MEDIUM

**Issue:** Transaction not atomic - partial failure leaves orphaned records.

```python
# Lines 412-413: Token created before email is sent
verification_token = EmailVerificationToken.objects.create(user=user)

# Lines 416-419: If email fails, user is deleted BUT token remains in orphaned state
except Exception as e:
    user.delete()  # User deleted but token may have issues
    messages.error(request, f"Failed to send verification email...")
```

**Problems:**
- If user deletion fails but appears to succeed, orphaned tokens exist
- EmailVerificationToken.user FK has CASCADE, but race conditions possible
- No atomic transaction wrapping the operation

**Impact:** Orphaned database records accumulate.

---

### BUG #8: Redundant student_id Field Not Properly Managed During Deletion
**File:** [complaints/models.py](complaints/models.py#L66-67)  
**Location:** Complaint model  
**Severity:** HIGH

**Issue:** Complaint model stores both `user` (ForeignKey) and `student_id` (BigIntegerField) to same user.

```python
# Line 33: Primary relationship
user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='complaints')

# Lines 66-67: Redundant manual storage of user ID
student_id = models.BigIntegerField(null=True, blank=True)
```

**In delete_user function:** [accounts/views.py](accounts/views.py#L809-810)
```python
# Line 809-810: Manual update needed because of redundant field
Complaint.objects.filter(student_id=user.id).update(student_id=None)
```

**Problems:**
- Two sources of truth for the same data
- If `user` is deleted, `student_id` becomes orphaned if code path changed
- Django CASCADE will delete Complaint objects, making student_id update pointless
- Violates DRY principle

**Impact:** Confusion about which field is authoritative; potential data integrity issues.

---

### BUG #9: Missing Atomic Transaction in delete_user()
**File:** [accounts/views.py](accounts/views.py#L788-850)  
**Location:** `delete_user()` function  
**Severity:** HIGH

**Issue:** Multiple database operations without atomic transaction wrapper.

```python
# Lines 804-829: Six separate update/delete operations with NO TRANSACTION
ComplaintResponse.objects.filter(staff_member=user).delete()
Complaint.objects.filter(assigned_to=user).update(assigned_to=None)
Complaint.objects.filter(student_id=user.id).update(student_id=None)
AdminQueue.objects.filter(reviewed_by=user).update(reviewed_by=None)
EmailVerificationToken.objects.filter(user=user).delete()
user.delete()
```

**Problems:**
- If database crashes between operations, partial deletion occurs
- No rollback if one operation fails
- Race conditions if user makes concurrent requests

**Example Failure Scenario:**
1. ComplaintResponse deleted successfully
2. Complaint.assigned_to set to NULL successfully
3. Admin crashes before user.delete()
4. User account partially deleted

**Impact:** Database corruption with orphaned records.

---

### BUG #10: Cascade Delete Chain Not Fully Tested
**File:** [complaints/models.py](complaints/models.py)  
**Location:** ComplaintResponse model, line 117  
**Severity:** MEDIUM

**Issue:** ComplaintResponse.staff_member has CASCADE delete, but when user deleted, cascade happens before explicit delete.

```python
# Line 117: CASCADE delete
staff_member = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
```

**In delete_user:** [accounts/views.py](accounts/views.py#L804)
```python
# Line 804: Explicit delete, but CASCADE will also trigger
ComplaintResponse.objects.filter(staff_member=user).delete()
```

**Problems:**
- Redundant deletion attempt
- If first explicit delete fails, CASCADE delete still happens
- No logging of what actually got deleted

**Impact:** Confusing behavior; difficult to debug what was actually deleted.

---

## 3. DATA INTEGRITY ISSUES

### BUG #11: Missing Validation in edit_user() - Email Uniqueness Case-Insensitive Not Enforced
**File:** [accounts/views.py](accounts/views.py#L862-875)  
**Location:** `edit_user()` function, line 866  
**Severity:** MEDIUM

**Issue:** Email update doesn't check for case-insensitive duplicates.

```python
# Line 866: Case-sensitive check only
if User.objects.filter(email=email).exclude(id=user.id).exists():
    messages.error(request, 'Email is already in use by another user')
```

**Scenario:**
- User A has email: "admin@example.com"
- Admin tries to update User B email to "ADMIN@EXAMPLE.COM"
- Check passes (case-sensitive)
- Both accounts now have same email (different cases)

**Impact:** Duplicate emails in database despite validation.

---

### BUG #12: No Validation for Required Fields in edit_user()
**File:** [accounts/views.py](accounts/views.py#L862-875)  
**Location:** `edit_user()` function, lines 862-875  
**Severity:** MEDIUM

**Issue:** No validation that staff/admin users have required fields set.

```python
# Lines 869-878: Allows saving staff/admin without department
first_name = request.POST.get('first_name', '').strip()
last_name = request.POST.get('last_name', '').strip()
email = request.POST.get('email', '').strip()
role = request.POST.get('role', user.role)

# No check that if role='staff', department must be set
user.role = role
user.save()
```

**Problems:**
- Staff users can be changed to have empty departments
- Breaks dashboard logic expecting department for staff
- Violates business rules

**Impact:** Staff dashboard failures due to missing department.

---

## SUMMARY TABLE

| # | Bug | Severity | Category | Impact |
|---|-----|----------|----------|--------|
| 1 | Missing Password Validation | HIGH | Registration | Weak passwords, security risk |
| 2 | Missing Email Validation | MEDIUM | Registration | Invalid emails stored |
| 3 | No Password Confirmation | MEDIUM | UX | User lockouts from typos |
| 4 | No Department Required for Staff | HIGH | Registration | Dashboard broken |
| 5 | No Role Validation | MEDIUM | Registration | Invalid roles created |
| 6 | Email Case Sensitivity | MEDIUM | Registration | Duplicate accounts |
| 7 | Orphaned Tokens on Email Failure | MEDIUM | Deletion | Database pollution |
| 8 | Redundant student_id Field | HIGH | Data Structure | Confusion, maintenance risk |
| 9 | Non-Atomic Delete Transaction | HIGH | Deletion | Database corruption risk |
| 10 | Cascade Delete Not Tested | MEDIUM | Deletion | Undefined behavior |
| 11 | Case-Insensitive Email in Edit | MEDIUM | Data Integrity | Duplicate emails |
| 12 | No Role-Based Field Validation | MEDIUM | Data Integrity | Invalid data states |

---

## RECOMMENDATIONS

### Immediate Fixes (P0 - Critical)
1. Add atomic transactions to delete_user()
2. Remove redundant student_id field
3. Add password validation
4. Enforce department field for staff/admin

### Short-term Fixes (P1 - High)
1. Add email format validation
2. Add role validation against ROLE_CHOICES
3. Add case-insensitive email check
4. Implement password confirmation field

### Long-term Improvements (P2 - Medium)
1. Create Django Forms for proper validation
2. Add comprehensive unit tests for deletion operations
3. Implement audit logging for data changes
4. Add database constraints at schema level
