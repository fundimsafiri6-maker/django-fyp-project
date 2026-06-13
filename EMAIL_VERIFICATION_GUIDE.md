# Email Verification Feature Documentation

## Overview
The email verification system ensures that students provide valid email addresses when registering for the AI Complaints System. This feature enhances account security and ensures proper communication channels with students.

## Features

### 1. **Student Registration Flow**
- Students sign up with their username, email, and password
- Account is created but **inactive** (cannot login)
- Verification email is automatically sent to the provided email address
- Student must click the verification link to activate their account

### 2. **Email Verification Process**
- Verification link sent to student's email address
- Link contains a unique, secure token (256-character URL-safe token)
- Token is valid for **24 hours**
- If token expires, student must sign up again
- Clicking the link activates the account and marks email as verified

### 3. **Login Protection**
- Students without verified emails **cannot login**
- They receive a message directing them to check their inbox
- Staff and Admin accounts can login normally (no email verification required)

## Implementation Details

### Database Models

#### User Model (Enhanced)
```python
class User(AbstractUser):
    is_email_verified = models.BooleanField(default=False)
```
- New field to track email verification status
- Default: `False` (unverified)

#### EmailVerificationToken Model
```python
class EmailVerificationToken(models.Model):
    user = OneToOneField(User)
    token = CharField(max_length=256, unique=True)
    created_at = DateTimeField(auto_now_add=True)
    expires_at = DateTimeField()
    
    def is_valid():  # Returns True if token hasn't expired
    def save():      # Auto-generates token and 24-hour expiry
```

### Views & Functions

#### 1. `register_view(request)`
**Location:** `accounts/views.py`

**Behavior:**
- Creates new user with `is_active=False` for students
- Generates `EmailVerificationToken`
- Sends verification email via `send_verification_email()`
- Returns success message prompting email check
- Staff/Admin accounts are immediately active

**Error Handling:**
- Duplicate username detection
- Duplicate email detection
- Email sending failures (user account deleted if email fails)

#### 2. `send_verification_email(request, user, verification_token)`
**Location:** `accounts/views.py`

**Behavior:**
- Builds verification URL with token
- Renders HTML email from template
- Sends via Django email backend
- Includes fallback plain text version

**Email Content:**
- Welcome message
- Verification link (clickable button + text)
- Token expiration warning
- Security warnings
- Support contact information

#### 3. `verify_email(request, token)`
**Location:** `accounts/views.py`
**URL:** `/accounts/verify-email/<token>/`

**Behavior:**
1. Validates token exists in database
2. Checks if token is still valid (not expired)
3. If valid:
   - Activates user account (`is_active=True`)
   - Marks email as verified (`is_email_verified=True`)
   - Deletes the token
   - Shows success message
4. If invalid or expired:
   - Shows error message
   - Renders status page with retry option

#### 4. `login_view(request)` (Enhanced)
**Location:** `accounts/views.py`

**Changes:**
- Checks if user's email is verified (for students only)
- Prevents login if email unverified
- Shows message directing to check email

### Email Templates

#### 1. HTML Email: `accounts/email_verification.html`
**Features:**
- Professional gradient header
- Clear call-to-action button
- Clickable link + text fallback
- Security warnings
- Expiration notice
- Support information

#### 2. Plain Text Email: `accounts/email_verification.txt`
**Features:**
- Fallback for text-only email clients
- Complete information and instructions

#### 3. Status Page: `accounts/verify_email_status.html`
**Features:**
- Success page: Shows checkmark, confirmation message, next steps
- Error page: Shows error icon, error message, retry options
- Responsive design
- Links to login and support

## URL Routes

```python
# In accounts/urls.py
path('verify-email/<str:token>/', views.verify_email, name='verify_email'),
```

**Example:** `http://localhost:8000/accounts/verify-email/AeB4tK9xL2m5pQ8rT1vW3yZ0aB7cD6eF9gH1jK4lM2nO5pQ7sT9uV2wX3yZ5aB.../`

## Email Configuration

### Development (Console Backend)
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'noreply@udom-complaints-system.ac.tz'
```
Emails are printed to console instead of sent.

### Production (SMTP Backend)
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # or your email provider
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
```

## User Experience

### Student Registration Flow
1. **Sign Up:** Student fills registration form
2. **Account Created:** System shows: "Account created! Check your email for verification link"
3. **Check Email:** Student receives email with verification link
4. **Click Link:** Student clicks link in email
5. **Verification:** System activates account and shows success page
6. **Login:** Student can now login with username/password

### Error Scenarios

**Scenario 1: Invalid Link**
- Message: "Invalid verification link"
- Action: User must sign up again

**Scenario 2: Expired Link (24+ hours)**
- Message: "Verification link has expired. Please sign up again"
- Account: Automatically deleted
- Action: User must sign up again with new email

**Scenario 3: No Verification, Attempt to Login**
- Message: "Please verify your email before signing in"
- Action: User checks inbox for verification email

**Scenario 4: Email Not Received**
- Action: User should sign up again with correct email
- Support: Contact support@udom-complaints.ac.tz

## Security Features

✅ **Secure Token Generation**
- Uses `secrets.token_urlsafe(64)` - cryptographically secure
- 256-character tokens
- Unique per account

✅ **Token Expiration**
- 24-hour validity period
- Expired accounts automatically cleaned up

✅ **Email Verification**
- Only verified emails can login (students)
- Prevents unauthorized access
- Ensures communication channel validity

✅ **One-Time Use**
- Token deleted after use
- Cannot be reused

✅ **Rate Limiting**
- Consider adding rate limiting for production
- Prevent brute force token guessing

## Testing the Feature

### Manual Testing (Development)

**1. Register as Student:**
```bash
1. Go to registration page
2. Fill form (username, email, password, role=student)
3. Check terminal/console for email output
4. Copy verification URL from console
5. Paste URL in browser
6. See success message
7. Try to login - should now work
```

**2. Test Token Expiration:**
```bash
1. Register new student
2. Note verification token in database
3. Go to Django admin: /admin/accounts/emailverificationtoken/
4. Change token's expires_at to past time
5. Try clicking link
6. Should see: "Verification link has expired"
```

**3. Test Invalid Token:**
```bash
1. Go to /accounts/verify-email/invalid-token-xyz/
2. Should see: "Invalid verification link"
3. Provided "Try Again" link to registration
```

### Unit Tests (Recommended)

```python
# In accounts/tests.py

def test_student_registration_creates_inactive_account():
    """Student accounts should be inactive until verified"""

def test_verification_email_sent_on_student_signup():
    """Email should be sent with verification token"""

def test_email_verification_activates_account():
    """Clicking verification link should activate account"""

def test_expired_token_prevents_verification():
    """Expired tokens should not verify accounts"""

def test_student_cannot_login_unverified():
    """Unverified students should not be able to login"""

def test_staff_signup_no_verification_needed():
    """Staff/Admin should not require email verification"""
```

## Database Migration

To apply the email verification feature to existing database:

```bash
# Run migrations
python manage.py migrate accounts

# This creates:
# 1. is_email_verified field on User model
# 2. EmailVerificationToken model
```

### Existing Users

For existing student accounts without email verification:
```python
# In Django shell
from accounts.models import User
User.objects.filter(role='student').update(is_email_verified=True, is_active=True)
```

## Future Enhancements

1. **Resend Verification Email**
   - Allow students to request new verification email
   - Useful if email was lost or spam folder

2. **Email Change Verification**
   - When student changes email, require re-verification

3. **Admin Override**
   - Admins can manually verify emails
   - Useful for bulk imports or special cases

4. **Audit Logging**
   - Track all verification attempts
   - Security monitoring

5. **Rate Limiting**
   - Limit signup and verification attempts
   - Prevent spam and brute force

6. **Webhook Integration**
   - Send verification status to external systems
   - Integration with student records system

## Troubleshooting

### Emails Not Sending?

1. **Check Email Backend Configuration**
   ```python
   # Development: Should be console backend
   EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
   ```

2. **Check Server Logs**
   ```bash
   # Look for email sending errors
   python manage.py runserver
   ```

3. **Production SMTP Issues**
   - Verify credentials
   - Check SMTP server availability
   - Look for firewall/network issues
   - Check email provider's security settings

### Verification Link Not Working?

1. **Check Token in Database**
   ```bash
   # Django admin: /admin/accounts/emailverificationtoken/
   # Verify token exists and hasn't expired
   ```

2. **Check URL Encoding**
   - Ensure token is copied correctly
   - Special characters might need encoding

3. **Check Email Header Links**
   - Ensure email client didn't break the link
   - Try copying raw link instead of clicking

## Admin Interface

### User Management
- Location: `/admin/accounts/user/`
- New fields: `is_email_verified`
- Filter by: Role, Active Status, Email Verification Status

### Token Management
- Location: `/admin/accounts/emailverificationtoken/`
- View: User, Token, Creation Date, Expiration Date
- Edit: Manually extend token expiration if needed

## Related Configuration Files

- **Settings:** `ai_complaints_system/settings.py`
- **Models:** `accounts/models.py`
- **Views:** `accounts/views.py`
- **URLs:** `accounts/urls.py`
- **Admin:** `accounts/admin.py`
- **Templates:** `templates/accounts/`
- **Migration:** `accounts/migrations/0002_email_verification.py`

## Support

For issues or questions:
- Email: support@udom-complaints.ac.tz
- Contact IT Help Desk
- Report bugs to development team
