from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import EmailVerificationToken
from complaints.models import Complaint, ComplaintResponse
import re

User = get_user_model()


class UserRegistrationTestCase(TestCase):
    """Test cases for user registration with validation"""
    
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
    
    def test_student_registration_success(self):
        """Test successful student registration with valid data"""
        data = {
            'username': 'testuser123',
            'email': 'test@example.com',
            'password': 'SecurePass123',
            'password_confirm': 'SecurePass123',
            'role': 'student',
        }
        response = self.client.post(self.register_url, data, follow=True)
        
        # Check user was created
        self.assertTrue(User.objects.filter(username='testuser123').exists())
        user = User.objects.get(username='testuser123')
        
        # Student should not be active until email verified
        self.assertFalse(user.is_active)
        self.assertEqual(user.role, 'student')
        self.assertFalse(user.is_email_verified)
        
        # Verification token should be created
        self.assertTrue(EmailVerificationToken.objects.filter(user=user).exists())
    
    def test_staff_registration_requires_department(self):
        """Test that staff registration requires department"""
        data = {
            'username': 'staffuser',
            'email': 'staff@example.com',
            'password': 'SecurePass123',
            'password_confirm': 'SecurePass123',
            'role': 'staff',
            'department': '',  # Missing department
        }
        response = self.client.post(self.register_url, data)
        
        # User should not be created
        self.assertFalse(User.objects.filter(username='staffuser').exists())
        # Error message should be shown
        self.assertContains(response, 'Department is required')
    
    def test_password_validation_too_short(self):
        """Test password validation for minimum length"""
        data = {
            'username': 'user1',
            'email': 'user1@example.com',
            'password': 'Short1',  # Too short
            'password_confirm': 'Short1',
            'role': 'student',
        }
        response = self.client.post(self.register_url, data)
        
        # User should not be created
        self.assertFalse(User.objects.filter(username='user1').exists())
        self.assertContains(response, '8 characters')
    
    def test_password_validation_no_uppercase(self):
        """Test password requires uppercase letter"""
        data = {
            'username': 'user2',
            'email': 'user2@example.com',
            'password': 'lowercase123',  # No uppercase
            'password_confirm': 'lowercase123',
            'role': 'student',
        }
        response = self.client.post(self.register_url, data)
        
        self.assertFalse(User.objects.filter(username='user2').exists())
        self.assertContains(response, 'uppercase')
    
    def test_password_validation_no_number(self):
        """Test password requires number"""
        data = {
            'username': 'user3',
            'email': 'user3@example.com',
            'password': 'NoNumbers',  # No numbers
            'password_confirm': 'NoNumbers',
            'role': 'student',
        }
        response = self.client.post(self.register_url, data)
        
        self.assertFalse(User.objects.filter(username='user3').exists())
        self.assertContains(response, 'number')
    
    def test_password_confirmation_mismatch(self):
        """Test password confirmation must match password"""
        data = {
            'username': 'user4',
            'email': 'user4@example.com',
            'password': 'SecurePass123',
            'password_confirm': 'DifferentPass123',  # Mismatch
            'role': 'student',
        }
        response = self.client.post(self.register_url, data)
        
        self.assertFalse(User.objects.filter(username='user4').exists())
        self.assertContains(response, 'not match')
    
    def test_email_case_insensitivity(self):
        """Test that email duplicates are prevented regardless of case"""
        # Create first user with lowercase email
        user1_data = {
            'username': 'user5',
            'email': 'test@example.com',
            'password': 'SecurePass123',
            'password_confirm': 'SecurePass123',
            'role': 'student',
        }
        response = self.client.post(self.register_url, user1_data, follow=True)
        self.assertTrue(User.objects.filter(email='test@example.com').exists())
        
        # Try to create second user with uppercase email (should fail)
        user2_data = {
            'username': 'user6',
            'email': 'TEST@EXAMPLE.COM',  # Same email, different case
            'password': 'SecurePass123',
            'password_confirm': 'SecurePass123',
            'role': 'student',
        }
        response = self.client.post(self.register_url, user2_data)
        
        self.assertFalse(User.objects.filter(username='user6').exists())
        self.assertContains(response, 'already registered')
    
    def test_username_validation_too_short(self):
        """Test username must be at least 3 characters"""
        data = {
            'username': 'ab',  # Too short
            'email': 'user@example.com',
            'password': 'SecurePass123',
            'password_confirm': 'SecurePass123',
            'role': 'student',
        }
        response = self.client.post(self.register_url, data)
        
        self.assertFalse(User.objects.filter(username='ab').exists())
        self.assertContains(response, '3 characters')
    
    def test_username_validation_invalid_characters(self):
        """Test username only allows alphanumeric and underscore"""
        data = {
            'username': 'user@123',  # Invalid character @
            'email': 'user@example.com',
            'password': 'SecurePass123',
            'password_confirm': 'SecurePass123',
            'role': 'student',
        }
        response = self.client.post(self.register_url, data)
        
        self.assertFalse(User.objects.filter(username='user@123').exists())
        self.assertContains(response, 'letters, numbers, and underscores')


class UserDeletionTestCase(TestCase):
    """Test cases for user deletion with cascade handling"""
    
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='AdminPass123',
            role='admin',
            is_active=True,
            is_staff=True
        )
        self.student_user = User.objects.create_user(
            username='student1',
            email='student@example.com',
            password='StudentPass123',
            role='student',
            is_active=True,
            is_email_verified=True
        )
        self.staff_user = User.objects.create_user(
            username='staff1',
            email='staff@example.com',
            password='StaffPass123',
            role='staff',
            is_active=True,
            department='academic'
        )
    
    def test_delete_user_with_complaints(self):
        """Test deleting user with complaints doesn't crash system"""
        # Create complaints for student
        complaint1 = Complaint.objects.create(
            title='Test Complaint 1',
            description='Test description',
            user=self.student_user,
            status='Pending',
            department='academic'
        )
        complaint2 = Complaint.objects.create(
            title='Test Complaint 2',
            description='Test description',
            user=self.student_user,
            status='In Progress',
            department='ict'
        )
        
        # Login as admin
        self.client.login(username='admin', password='AdminPass123')
        
        # Delete user
        response = self.client.post(
            reverse('delete_user', args=[self.student_user.id]),
            follow=True
        )
        
        # Check user is deleted
        self.assertFalse(User.objects.filter(id=self.student_user.id).exists())
        
        # Check complaints are also deleted (CASCADE)
        self.assertFalse(Complaint.objects.filter(user__id=self.student_user.id).exists())
    
    def test_delete_staff_assigned_complaints(self):
        """Test deleting staff member reassigns their complaints"""
        # Create complaint assigned to staff
        complaint = Complaint.objects.create(
            title='Test Complaint',
            description='Test description',
            user=self.student_user,
            assigned_to=self.staff_user,
            status='In Progress',
            department='academic'
        )
        
        # Login as admin
        self.client.login(username='admin', password='AdminPass123')
        
        # Delete staff user
        response = self.client.post(
            reverse('delete_user', args=[self.staff_user.id]),
            follow=True
        )
        
        # Staff should be deleted
        self.assertFalse(User.objects.filter(id=self.staff_user.id).exists())
        
        # Complaint should still exist but assigned_to should be null
        complaint.refresh_from_db()
        self.assertIsNone(complaint.assigned_to)
    
    def test_delete_user_with_responses(self):
        """Test deleting staff member deletes their complaint responses"""
        complaint = Complaint.objects.create(
            title='Test Complaint',
            description='Test description',
            user=self.student_user,
            assigned_to=self.staff_user,
            status='In Progress',
            department='academic'
        )
        
        response = ComplaintResponse.objects.create(
            complaint=complaint,
            staff_member=self.staff_user,
            response='Staff response'
        )
        
        # Login as admin
        self.client.login(username='admin', password='AdminPass123')
        
        # Delete staff user
        self.client.post(
            reverse('delete_user', args=[self.staff_user.id]),
            follow=True
        )
        
        # Response should be deleted
        self.assertFalse(ComplaintResponse.objects.filter(id=response.id).exists())
    
    def test_cannot_delete_own_account(self):
        """Test user cannot delete their own account"""
        self.client.login(username='admin', password='AdminPass123')
        
        # Try to delete own account
        response = self.client.post(
            reverse('delete_user', args=[self.admin_user.id]),
            follow=True
        )
        
        # Admin should still exist
        self.assertTrue(User.objects.filter(id=self.admin_user.id).exists())
        self.assertContains(response, 'cannot delete your own account')


class UserEditTestCase(TestCase):
    """Test cases for user editing"""
    
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='AdminPass123',
            role='admin',
            is_active=True,
            is_staff=True
        )
        self.student_user = User.objects.create_user(
            username='student1',
            email='student@example.com',
            password='StudentPass123',
            role='student',
            is_active=True,
            is_email_verified=True
        )
    
    def test_edit_email_case_insensitive(self):
        """Test that email edit prevents case-insensitive duplicates"""
        # Create another student with different case email
        user2 = User.objects.create_user(
            username='student2',
            email='test@example.com',
            password='StudentPass123',
            role='student'
        )
        
        # Login as admin
        self.client.login(username='admin', password='AdminPass123')
        
        # Try to change student1's email to uppercase version of student2's email
        data = {
            'first_name': 'Student',
            'last_name': 'One',
            'email': 'TEST@EXAMPLE.COM',  # Different case
            'role': 'student'
        }
        response = self.client.post(
            reverse('edit_user', args=[self.student_user.id]),
            data
        )
        
        # Edit should fail
        self.assertContains(response, 'already in use')
    
    def test_promote_student_to_staff_requires_department(self):
        """Test that promoting to staff requires department"""
        self.client.login(username='admin', password='AdminPass123')
        
        data = {
            'first_name': 'Student',
            'last_name': 'One',
            'email': 'student@example.com',
            'role': 'staff',
            'department': ''  # Missing department
        }
        response = self.client.post(
            reverse('edit_user', args=[self.student_user.id]),
            data
        )
        
        # Edit should fail
        self.student_user.refresh_from_db()
        self.assertEqual(self.student_user.role, 'student')  # Should still be student
        self.assertContains(response, 'Department is required')
