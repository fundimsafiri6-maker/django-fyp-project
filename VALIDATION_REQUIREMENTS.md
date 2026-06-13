# 🔐 User Validation Requirements - Quick Reference

## Registration Form Requirements

### For All Users
| Field | Requirement | Example |
|-------|-------------|---------|
| Username | 3+ chars, only `[a-zA-Z0-9_]` | `john_doe_123` ✅ |
| Email | Valid email format, unique (case-insensitive) | `john@example.com` ✅ |
| Password | 8+ chars with uppercase, lowercase, number | `SecurePass123` ✅ |
| Confirm Password | Must match password field | Match required |

### For Staff & Admin Only
| Field | Requirement | Example |
|-------|-------------|---------|
| Department | Required selection | academic, ict, admin, student_affairs, other |
| Registration Number | Optional | `EMP123456` or empty |

### For Students Only
| Field | Requirement | Example |
|-------|-------------|---------|
| Department | Not shown/optional | N/A |
| Registration Number | Optional | `STU123456` or empty |

---

## Common Validation Errors & Fixes

### ❌ Error: "Username must be at least 3 characters long"
**Fix:** Use 3 or more characters
- ❌ `ab`, `a1`
- ✅ `john`, `user_123`, `test_001`

### ❌ Error: "Username can only contain letters, numbers, and underscores"
**Fix:** Remove special characters
- ❌ `john@123`, `user-name`, `john.doe`
- ✅ `john123`, `user_name`, `johndoe`

### ❌ Error: "Invalid email format"
**Fix:** Use proper email format
- ❌ `user@`, `user@.com`, `user@domain`
- ✅ `user@example.com`, `john.doe@company.org`

### ❌ Error: "Email already registered"
**Fix:** Email exists (case-insensitive), use different email
- ❌ Trying `john@EXAMPLE.COM` when `john@example.com` exists
- ✅ Use `john2@example.com` or `different@domain.com`

### ❌ Error: "Password must be at least 8 characters long"
**Fix:** Use 8+ character password
- ❌ `Pass1`, `Test12`
- ✅ `SecurePass123`, `MyPassword2024`

### ❌ Error: "Password must contain at least one uppercase letter"
**Fix:** Add uppercase letter
- ❌ `securepass123`
- ✅ `SecurePass123`

### ❌ Error: "Password must contain at least one lowercase letter"
**Fix:** Add lowercase letter
- ❌ `SECUREPASS123`
- ✅ `SecurePass123`

### ❌ Error: "Password must contain at least one number"
**Fix:** Add number
- ❌ `SecurePassword`
- ✅ `SecurePass123`

### ❌ Error: "Passwords do not match"
**Fix:** Enter same password in both password fields
- Make sure "Password" and "Confirm Password" fields are identical

### ❌ Error: "Department is required for staff users"
**Fix:** Select department when user type is "Staff Member"
1. Select "Staff Member" from User Type dropdown
2. Department dropdown appears
3. Select: Academic, ICT, Administration, Student Affairs, or Other

### ❌ Error: "Department is required for admin users"
**Fix:** Select department when user type is "Administrator"
- Same as staff - department selection becomes required

### ❌ Error: "Invalid role selected"
**Fix:** Only use valid roles
- ✅ Valid: student, staff, admin
- ❌ Invalid: teacher, moderator, superuser

---

## User Types & Required Fields

### 👨‍🎓 Student
```
✅ Required:
   - Username
   - Email
   - Password
   
⚠️ Optional:
   - Registration Number
   - Department (shown but not required)

ℹ️ Notes:
   - Account inactive until email verified
   - Verification email sent automatically
```

### 👨‍💼 Staff Member
```
✅ Required:
   - Username
   - Email
   - Password
   - Department
   
⚠️ Optional:
   - Registration Number

ℹ️ Notes:
   - Account active immediately
   - Can only see complaints for their department
   - Can assign complaints to themselves
```

### 🔐 Administrator
```
✅ Required:
   - Username
   - Email
   - Password
   - Department
   
⚠️ Optional:
   - Registration Number

ℹ️ Notes:
   - Account active immediately
   - Can manage all users
   - Can see system-wide statistics
   - Can access all departments
```

---

## Department Selection

### Valid Departments
| Code | Display Name | Purpose |
|------|--------------|---------|
| `academic` | Academic | Academic complaints |
| `ict` | ICT | Technology & systems |
| `admin` | Administration | Administrative issues |
| `student_affairs` | Student Affairs | Student services |
| `other` | Other | Miscellaneous |

**Note:** Department is only required for Staff and Admin users. Students don't need to select department.

---

## Password Requirements

### Good Password Examples ✅
- `SecurePass123` - Uppercase + lowercase + number
- `MyPassword2024` - Clear, strong, memorable
- `Welcome_2024!` - Special characters not required but allowed
- `CompanyId_001` - Work-related but still strong

### Bad Password Examples ❌
- `password` - No uppercase, no number
- `Pass123` - Only 7 characters (need 8+)
- `123456789` - No letters
- `UPPERCASE` - No lowercase, no number
- `abc` - Too short, no number

---

## API/Django Admin Notes

### Creating Users via Django Admin
If creating users through Django admin panel:

```python
# For Students
user = User.objects.create_user(
    username='john_doe',
    email='john@example.com',
    password='SecurePass123',
    role='student',
    is_active=False,  # Wait for email verification
    is_email_verified=False
)

# For Staff
user = User.objects.create_user(
    username='staff_member',
    email='staff@example.com',
    password='SecurePass123',
    role='staff',
    department='academic',  # REQUIRED
    is_active=True
)

# For Admin
user = User.objects.create_user(
    username='admin_user',
    email='admin@example.com',
    password='SecurePass123',
    role='admin',
    department='academic',  # REQUIRED
    is_active=True,
    is_staff=True
)
```

### Editing Users via Django Admin
When editing users through Django admin:

1. **Email changes**: Will be case-normalized to lowercase
2. **Role changes**: 
   - Student → Staff/Admin: **Department becomes required**
   - Staff/Admin → Student: Department will be cleared
3. **Department changes**: Affects what complaints user can see
4. **Activation**: 
   - Admin/Staff: Can activate immediately
   - Students: Only activate after email verification

---

## Troubleshooting

### User Created But Can't Login
**Check:**
- ✅ Is account active? (Students need email verification first)
- ✅ Did you enter correct password?
- ✅ Is email verified for students?

**Solution:**
- For students: Check email for verification link
- Use "Resend Verification Email" if needed
- Admin can manually verify email in admin panel

### User Deleted But Got Error
**Possible Causes:**
- ❌ Trying to delete own account (not allowed)
- ❌ Database integrity issue

**Solution:**
- Check error message carefully
- Try again after page refresh
- Contact admin if persists

### Department Not Showing
**Cause:** User is student (department only for staff/admin)

**Solution:**
- Select "Staff Member" or "Administrator" in User Type
- Department field will appear
- Select appropriate department

---

## Best Practices

1. **Use meaningful usernames**
   - ✅ `john_smith_001`, `jane_doe`
   - ❌ `user123`, `test`

2. **Use work email for staff/admin**
   - ✅ `john@company.edu`, `staff@university.org`
   - ❌ `john@gmail.com` (for staff accounts)

3. **Assign correct department immediately**
   - Creates correct access controls
   - Ensures staff see only relevant complaints

4. **Never use same password twice**
   - Generate strong, unique passwords
   - Use password manager for storage

5. **Regular password updates**
   - Request password changes periodically
   - More frequently for admin accounts

---

**Last Updated:** May 13, 2026
**Version:** 1.0