from django.contrib import admin
from .models import AIAnalysisResult
@admin.register(AIAnalysisResult)
class AIAnalysisResultAdmin(admin.ModelAdmin):
    list_display = (
        'complaint',
        'predicted_category',
        'sentiment',
        'urgency_score',
        'processed_at',
    )
    list_filter = ('predicted_category', 'sentiment')
