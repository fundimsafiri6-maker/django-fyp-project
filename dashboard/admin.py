from django.contrib import admin
from .models import ComplaintStatistics
@admin.register(ComplaintStatistics)
class ComplaintStatisticsAdmin(admin.ModelAdmin):
    list_display = (
        'date',
        'total_complaints',
        'resolved_complaints',
        'pending_complaints',
    )
