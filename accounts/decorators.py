# Role-based access control decorators
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def student_required(view_func):
    """Decorator to restrict view to students only"""
    @wraps(view_func)
    @login_required(login_url='login')
    def wrapper(request, *args, **kwargs):
        if request.user.role != 'student':
            messages.error(request, 'Only students can access this feature')
            return redirect('student_dashboard') if request.user.role == 'student' else \
                   redirect('staff_dashboard') if request.user.role == 'staff' else \
                   redirect('hod_dashboard') if request.user.role == 'hod' else \
                   redirect('admin_dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper

def staff_required(view_func):
    """Decorator to restrict view to staff only"""
    @wraps(view_func)
    @login_required(login_url='login')
    def wrapper(request, *args, **kwargs):
        if request.user.role not in ['staff', 'hod']:
            messages.error(request, 'Only staff can access this feature')
            return redirect('student_dashboard') if request.user.role == 'student' else \
                   redirect('hod_dashboard') if request.user.role == 'hod' else \
                   redirect('admin_dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper

def admin_required(view_func):
    """Decorator to restrict view to admin only"""
    @wraps(view_func)
    @login_required(login_url='login')
    def wrapper(request, *args, **kwargs):
        if request.user.role != 'admin':
            messages.error(request, 'Only administrators can access this feature')
            return redirect('student_dashboard') if request.user.role == 'student' else \
                   redirect('staff_dashboard') if request.user.role == 'staff' else \
                   redirect('hod_dashboard') if request.user.role == 'hod' else \
                   redirect('admin_dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper

def staff_or_admin_required(view_func):
    """Decorator to restrict view to staff, HOD, or admin"""
    @wraps(view_func)
    @login_required(login_url='login')
    def wrapper(request, *args, **kwargs):
        if request.user.role not in ['staff', 'hod', 'admin']:
            messages.error(request, 'Only staff, HOD, and administrators can access this feature')
            return redirect('student_dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper
