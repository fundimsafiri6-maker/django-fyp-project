from django.shortcuts import render, get_object_or_404
from .models import AIAnalysisResult
from complaints.models import Complaint
def ai_result_view(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)
    ai_result = AIAnalysisResult.objects.filter(complaint=complaint).first()

    return render(request, 'ai_engine/ai_classification.html', {
        'complaint': complaint,
        'ai_result': ai_result
    })
