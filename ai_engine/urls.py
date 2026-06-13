from django.urls import path
from . import views

urlpatterns = [
    path('result/<int:complaint_id>/', views.ai_result_view, name='ai_result'),
]
