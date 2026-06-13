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
        text = f"{complaint.description} {complaint.title}" if complaint.description else complaint.title

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
    """

    @classmethod
    def assign_to_staff(cls, complaint, staff_member=None):
        from accounts.models import User

        if staff_member:
            if complaint.department == 'hod':
                if staff_member.role == 'hod':
                    complaint.assigned_to = staff_member
                else:
                    logger.warning(f"Cannot assign HOD complaint {complaint.id} to {staff_member.username}")
            elif complaint.department == 'other':
                if staff_member.role == 'admin':
                    complaint.assigned_to = staff_member
                else:
                    logger.warning(f"Cannot assign Other complaint {complaint.id} to {staff_member.username}")
            elif staff_member.role == 'staff' and staff_member.department == complaint.department:
                complaint.assigned_to = staff_member
            else:
                logger.warning(f"Cannot assign complaint {complaint.id} to {staff_member.username}")
            complaint.save()
            return complaint

        if not complaint.department:
            complaint.save()
            return complaint

        if complaint.department == 'hod':
            users = User.objects.filter(role='hod').annotate(
                cnt=models.Count('assigned_complaints')).order_by('cnt')
            if users.exists():
                complaint.assigned_to = users.first()
        elif complaint.department == 'other':
            users = User.objects.filter(role='admin').annotate(
                cnt=models.Count('assigned_complaints')).order_by('cnt')
            if users.exists():
                complaint.assigned_to = users.first()
        else:
            users = User.objects.filter(role='staff',
                department=complaint.department).annotate(
                cnt=models.Count('assigned_complaints')).order_by('cnt')
            if users.exists():
                complaint.assigned_to = users.first()

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
