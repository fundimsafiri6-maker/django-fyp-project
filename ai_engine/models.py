from django.db import models
from complaints.models import Complaint
class AIAnalysisResult(models.Model):
    complaint = models.OneToOneField(
        Complaint, on_delete=models.CASCADE
    )

    predicted_category = models.CharField(max_length=100)
    sentiment = models.CharField(max_length=50)
    urgency_score = models.FloatField()

    processed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"AI Result for Complaint #{self.complaint.id}"
