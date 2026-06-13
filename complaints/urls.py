from django.urls import path
from . import views

urlpatterns = [
    path('submit-complaint/', views.submit_complaint, name='submit_complaint'),
    path('my-complaints/', views.my_complaints, name='my_complaints'),
    path('complaint-detail/<int:id>/', views.complaint_detail, name='complaint_detail'),
    path('complaint-update/<int:id>/', views.complaint_update, name='complaint_update'),
    path('complaint-delete/<int:id>/', views.delete_complaint, name='delete_complaint'),
    path('staff-respond/<int:id>/', views.staff_respond, name='staff_respond'),
    path('assign-complaints/', views.assign_complaints, name='assign_complaints'),
    path('complaints-stats/', views.complaints_stats, name='complaints_stats'),
]
