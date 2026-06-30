"""
AI Complaint Classification and Routing Service

Uses the trained LogisticRegression model + rule-based pipeline from classifier.py.
Workflow: ICT outage rule -> Other rule -> ML model -> HOD check -> low-confidence fallback.
Returns category (Academic/ICT/Other/HOD) with priority and confidence.
"""

import logging
from django.db import models
from .models import Complaint
from .classifier import classify_complaint as _classify_text

logger = logging.getLogger(__name__)

CATEGORY_DEPT_MAP = {
    'Academic': 'academic',
    'ICT': 'ict',
    'HOD': 'hod',
    'Other': 'other',
}

PRIORITY_MAP = {
    'high': 'High',
    'medium': 'Medium',
    'low': 'Low',
}


class ComplaintClassifier:
    """
    Classifies complaints using the improved LogisticRegression pipeline.
    Delegates to classifier.py for all classification logic.
    """

    @classmethod
    def classify_complaint(cls, complaint):
        """
        Classify a complaint using the full pipeline (rules + ML + HOD).
        Args:
            complaint: Complaint instance (reads title + description)
        Returns:
            dict with keys: department, confidence_score, priority, reason
        """
        text = complaint.description if complaint.description else complaint.title

        try:
            result = _classify_text(text)
            cat = result['category']
            dept = CATEGORY_DEPT_MAP.get(cat, 'other')
            raw_pri = result.get('routing_priority', 'normal')
            pri = PRIORITY_MAP.get(raw_pri, 'Medium')
            conf = float(result.get('confidence', result.get('ml_confidence', 0.85)))
            reason = result.get('reason', '')

            return {
                'department': dept,
                'confidence_score': min(conf, 1.0),
                'priority': pri,
                'reason': reason,
                'method': 'Pipeline'
            }
        except Exception as e:
            logger.error(f"Classification error: {e}")
            return {
                'department': 'other',
                'confidence_score': 0.0,
                'priority': 'Medium',
                'reason': f'Classification error: {e}',
                'method': 'Error'
            }

    @classmethod
    def process_complaint(cls, complaint):
        """Classify complaint, update its department/priority/confidence, save."""
        classification = cls.classify_complaint(complaint)
        complaint.department = classification['department']
        complaint.priority = classification['priority']
        complaint.ai_confidence_score = classification['confidence_score']
        complaint.ai_classified = True
        complaint.save()
        return complaint


class DepartmentRouter:
    """
    Routes complaints to appropriate staff/HOD/admin based on department.
    Auto-creates default staff if none exist for a department.
    """

    DEFAULT_STAFF = {
        'academic': {
            'username': 'lucy',
            'first_name': 'Lucy',
            'last_name': 'Academic Staff',
            'email': 'lucy@udom.ac.tz',
            'role': 'staff',
            'department': 'academic',
        },
        'ict': {
            'username': 'tech_support',
            'first_name': 'Tech',
            'last_name': 'Support',
            'email': 'tech_support@udom.ac.tz',
            'role': 'staff',
            'department': 'ict',
        },
        'other': {
            'username': 'admin_officer',
            'first_name': 'Admin',
            'last_name': 'Officer',
            'email': 'admin_officer@udom.ac.tz',
            'role': 'admin',
            'department': 'other',
        },
    }

    @classmethod
    def _get_or_create_staff(cls, department_code, role, username_filter=None):
        """Find existing staff or auto-create default for department."""
        from accounts.models import User

        if department_code == 'hod':
            users = User.objects.filter(role='hod').annotate(
                cnt=models.Count('assigned_complaints')).order_by('cnt')
        else:
            base = User.objects.filter(role=role, department__iexact=department_code)
            if username_filter:
                base = base.filter(
                    models.Q(username__in=username_filter) |
                    models.Q(first_name__iexact=username_filter[0])
                )
            users = base.annotate(
                cnt=models.Count('assigned_complaints')).order_by('cnt')

        if users.exists():
            return users.first()

        defaults = cls.DEFAULT_STAFF.get(department_code)
        if not defaults:
            return None

        if User.objects.filter(username=defaults['username']).exists():
            return User.objects.get(username=defaults['username'])

        user = User.objects.create_user(
            username=defaults['username'],
            email=defaults['email'],
            password='staff123',
            first_name=defaults['first_name'],
            last_name=defaults['last_name'],
            role=defaults['role'],
            department=defaults['department'],
            is_active=True,
        )
        logger.info(f"Auto-created default {department_code} staff: {user.username} ({user.email})")
        return user

    @classmethod
    def assign_to_staff(cls, complaint, staff_member=None):
        from accounts.models import User

        if staff_member:
            valid = False
            if complaint.department == 'hod' and staff_member.role == 'hod':
                valid = True
            elif complaint.department == 'other' and staff_member.role == 'admin':
                valid = True
            elif staff_member.role == 'staff' and staff_member.department == complaint.department:
                valid = True

            if valid:
                complaint.assigned_to = staff_member
            else:
                logger.warning(
                    f"Cannot assign complaint {complaint.id} to {staff_member.username} "
                    f"(role={staff_member.role}, dept={staff_member.department})"
                )
            complaint.save()
            return complaint

        if not complaint.department:
            complaint.save()
            return complaint

        if complaint.department == 'hod':
            user = cls._get_or_create_staff('hod', 'hod')
        elif complaint.department == 'other':
            user = cls._get_or_create_staff('other', 'admin')
        elif complaint.department == 'academic':
            user = cls._get_or_create_staff(
                'academic', 'staff',
                username_filter=['lucy', 'lucia', 'lucy_m']
            )
        else:
            user = cls._get_or_create_staff(complaint.department, 'staff')

        if user:
            complaint.assigned_to = user

        complaint.save()
        return complaint

    @classmethod
    def get_department_staff(cls, department_code):
        from accounts.models import User
        if department_code == 'hod':
            return User.objects.filter(role='hod').order_by('first_name', 'last_name')
        return User.objects.filter(role='staff', department=department_code).order_by('first_name', 'last_name')

    @classmethod
    def get_department_complaints(cls, department_code):
        return Complaint.objects.filter(department=department_code).order_by('-created_at')
