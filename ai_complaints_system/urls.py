from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def home_redirect(request):
    return redirect('login')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('ai/', include('ai_engine.urls')),
    path('', include('complaints.urls')),
    path('', home_redirect),
    
]
