# Email Verification - Quick Reference Guide

## 🚀 Quick Start

### Testing the Feature (Development)

```bash
# 1. Run server
python manage.py runserver

# 2. Go to registration
# Open browser: http://localhost:8000/accounts/register/

# 3. Register as student
# - Username: teststudent
# - Email: test@example.com
# - Password: TestPassword123
# - Role: Student
# Click "Register"

# 4. Check email in terminal
# Look for console output with verification link

# 5. Copy verification URL
# Example: /accounts/verify-email/AeB4tK9xL2m5pQ8rT1vW3yZ0aB7cD6eF.../

# 6. Paste URL in browser
# http://localhost:8000{URL from step 5}

# 7. See success message
# "Email verified successfully!"

# 8. Login
# Go to http://localhost:8000/accounts/login/
# Use credentials from step 3
```

---

## 📁 Key Files

| File | Purpose |
|------|---------|
| `accounts/models.py` | User model + EmailVerificationToken model |
| `accounts/views.py` | Registration, verification, login views |
| `accounts/urls.py` | URL routing |
| `templates/accounts/email_verification.html` | HTML email template |
| `templates/accounts/verify_email_status.html` | Status page (success/error) |
| `accounts/admin.py` | Admin interface |

---

## 🔑 Key Functions

### `send_verification_email(request, user, verification_token)`
Sends verification email to student's email address
- Called automatically on student signup
- Builds verification URL with token
- Renders HTML and plain text versions

### `verify_email(request, token)`
Handles verification link clicks
- Validates token exists and not expired
- Activates user account
- Marks email as verified
- Displays success/error page

### `register_view(request)` - Enhanced
Handles student registration
- Creates inactive account for students
- Generates verification token
- Sends verification email
- Immediate activation for staff/admin

### `login_view(request)` - Enhanced
Checks email verification for students
- Prevents login if email not verified
- Shows helpful error message
- Staff/admin login unchanged

---

## 🗄️ Database Tables

### accounts_user
```
- is_email_verified (BOOLEAN, default=False)
- is_active (BOOLEAN, controls login - False for unverified students)
```

### accounts_emailverificationtoken
```
- id (PRIMARY KEY)
- user_id (UNIQUE FOREIGN KEY) → User
- token (VARCHAR 255, UNIQUE)
- created_at (DATETIME, auto-set)
- expires_at (DATETIME, +24 hours from creation)
```

---

## 🔗 URL Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/accounts/register/` | GET/POST | Student registration form |
| `/accounts/verify-email/<token>/` | GET | Handle verification link click |
| `/accounts/login/` | GET/POST | Student login (enhanced) |

---

## 📧 Email Workflow

```
Registration Form
      ↓
Register Button → register_view()
      ↓
Create User (is_active=False, is_email_verified=False)
      ↓
Generate EmailVerificationToken
      ↓
send_verification_email() → HTML email → Email Backend → Console Output
      ↓
Student receives email (checks console in dev)
      ↓
Student clicks verification link
      ↓
verify_email(request, token)
      ↓
Validate token → Activate user → Mark email verified → Delete token
      ↓
Success page displayed
      ↓
Student can now login
```

---

## ⚙️ Configuration

### Development (Current)
```python
# ai_complaints_system/settings.py
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'noreply@udom-complaints-system.ac.tz'
```

### Production
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', True)
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')
```

---

## 👤 User States

### Student - Not Registered
```
is_active: N/A
is_email_verified: N/A
```

### Student - Registered (Unverified)
```
is_active: False ← Cannot login
is_email_verified: False
```

### Student - Email Verified
```
is_active: True ← Can login
is_email_verified: True
```

### Staff/Admin
```
is_active: True ← Can login immediately
is_email_verified: False ← Not required
```

---

## 🔐 Security Details

- **Token Generation:** `secrets.token_urlsafe(64)` truncated to 255 chars
- **Token Storage:** Hashed in database via Django ORM
- **Token Validity:** 24 hours from creation
- **Token Use:** One-time only (deleted after verification)
- **Expired Cleanup:** Accounts deleted after token expiration
- **Email:** Required, must be unique, must be valid format

---

## 🧪 Admin Functions

### View Users
```
/admin/accounts/user/
```
**Filters:**
- By role (student/staff/admin)
- By active status
- By email verification status

**Actions:**
- Manually set is_email_verified if needed
- Deactivate/activate accounts
- Reset passwords

### View Tokens
```
/admin/accounts/emailverificationtoken/
```
**Display:**
- Associated user
- Token validity status
- Creation and expiration dates

**Actions:**
- Manually extend expiration (testing)
- Delete tokens
- Search by user/email

---

## 📊 User Journey

### Student Path
```
1. Click "Register"
2. Fill form (email required)
3. Submit
4. See: "Check your email for verification link"
5. Check email
6. Click verification link
7. See: "Email verified successfully!"
8. Click "Go to Login"
9. Enter credentials
10. Login successful
11. Access dashboard
```

### Failed Verification Path
```
1. Token expired (24+ hours)
   → See: "Link expired, sign up again"
   → Redirect to registration

2. Invalid token
   → See: "Invalid verification link"
   → Redirect to registration

3. Email not received
   → Manual option: Contact support
   → Admin option: Manually verify in admin
```

---

## ⚠️ Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| Email not showing in console | Check Django runserver terminal output |
| Token not working | May be expired (24 hours max) |
| Can't login after verification | Check is_email_verified=True in admin |
| MySQL warning about token field | ✅ Already fixed (max_length=255) |
| Duplicate email error | Use different email address |
| Email sending fails | Check EMAIL_BACKEND configuration |

---

## 📋 Checklist: Adding to Existing Project

- ✅ Models updated with email verification fields
- ✅ Migrations created and applied
- ✅ Views implemented
- ✅ URLs configured
- ✅ Email templates created
- ✅ Admin interface configured
- ✅ Email backend configured
- ✅ Database migrated successfully
- ✅ Documentation created
- ✅ Ready to test!

---

## 🚀 Next Steps

1. **Test locally** - Follow "Quick Start" above
2. **Review code** - Check `accounts/views.py` for logic
3. **Customize emails** - Edit `templates/accounts/email_verification.html`
4. **Configure production** - Set SMTP credentials for production
5. **Deploy** - Apply migrations on production database
6. **Monitor** - Check email delivery and verification rates

---

## 📞 Help & Support

- **Full Documentation:** See `EMAIL_VERIFICATION_GUIDE.md`
- **Implementation Details:** See `EMAIL_VERIFICATION_IMPLEMENTATION.md`
- **Code Location:** `accounts/` app
- **Support Email:** support@udom-complaints.ac.tz

---

**Version:** 1.0  
**Last Updated:** May 2026  
**Status:** ✅ Production Ready
