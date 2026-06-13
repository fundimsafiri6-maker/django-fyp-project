from django.db import models
from complaints.models import Complaint
class ComplaintStatistics(models.Model):
    date = models.DateField(auto_now_add=True)
    total_complaints = models.PositiveIntegerField()
    resolved_complaints = models.PositiveIntegerField()
    pending_complaints = models.PositiveIntegerField()

    def __str__(self):
        return f"Statistics for {self.date}"
