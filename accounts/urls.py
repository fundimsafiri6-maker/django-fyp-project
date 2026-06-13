from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('verify-email/<str:token>/', views.verify_email, name='verify_email'),
    path('resend-verification/', views.resend_verification_email, name='resend_verification'),
    path('profile/', views.user_profile, name='user_profile'),
    path('settings/', views.settings_page, name='settings'),
    path('help/', views.help_page, name='help'),

    # Chatbot API
    path('api/chatbot-search/', views.chatbot_search, name='chatbot_search'),

    # Dashboard views
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('staff-dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('hod-dashboard/', views.hod_dashboard, name='hod_dashboard'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),

    # Department-specific dashboards
    path('academic-dashboard/', views.academic_department_dashboard, name='academic_dashboard'),
    path('ict-dashboard/', views.ict_department_dashboard, name='ict_dashboard'),

    # Admin features
    path('admin-users/', views.admin_users, name='admin_users'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('edit-user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('admin-analytics/', views.admin_analytics, name='admin_analytics'),
    path('admin-analytics-pdf/', views.admin_analytics_pdf, name='admin_analytics_pdf'),
    path('report/', views.report_page, name='report_page'),
]
