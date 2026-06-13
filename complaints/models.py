from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


class Complaint(models.Model):

    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
        ('Rejected', 'Rejected'),
    )

    PRIORITY_CHOICES = (
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Urgent', 'Urgent'),
    )

    DEPARTMENT_CHOICES = (
        ('academic', 'Academic'),
        ('ict', 'ICT'),
        ('hod', 'HOD'),
        ('other', 'Other'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=100, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='complaints')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='Medium')
    attachment = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Department routing - for staff to handle complaints by department
    department = models.CharField(
        max_length=20, 
        choices=DEPARTMENT_CHOICES, 
        null=True, 
        blank=True,
        help_text="Department this complaint is routed to"
    )
    
    # AI Classification confidence score (0-100)
    ai_confidence_score = models.FloatField(
        default=0.0,
        help_text="AI model confidence score for classification (0-100)"
    )
    
    # Assign staff member to handle the complaint
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='assigned_complaints'
    )
    
    # student_id is a reference to User ID
    student_id = models.BigIntegerField(null=True, blank=True)
    
    # Track if complaint was AI-classified
    ai_classified = models.BooleanField(
        default=False,
        help_text="Whether this complaint was processed by AI classifier"
    )

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']


class ComplaintResponse(models.Model):
    """Model to store staff responses to complaints"""
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='responses')
    staff_member = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Response to {self.complaint.title} by {self.staff_member.username}"
    
    class Meta:
        ordering = ['-created_at']


class AdminQueue(models.Model):
    """Model for tracking complaints that require admin review"""
    REVIEW_STATUS = (
        ('pending_review', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('deleted', 'Deleted'),
    )
    
    complaint = models.OneToOneField(
        Complaint, 
        on_delete=models.CASCADE, 
        related_name='admin_queue',
        null=True,
        blank=True
    )
    complaint_text = models.TextField(help_text="Full complaint text for review")
    category = models.CharField(max_length=50, help_text="Classification category (usually 'Other')")
    reason = models.TextField(help_text="Reason why this complaint requires admin review")
    status = models.CharField(
        max_length=20, 
        choices=REVIEW_STATUS, 
        default='pending_review'
    )
    reviewed_by = models.ForeignKey(
        User, 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL,
        related_name='reviewed_admin_queue'
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True, help_text="Admin notes on review")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.status} - {self.complaint_text[:50]}"


class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message[:50]}"

