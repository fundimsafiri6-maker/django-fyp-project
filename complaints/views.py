from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from .models import Complaint, ComplaintResponse, Notification
from .ai_classifier import ComplaintClassifier, DepartmentRouter
from .email_utils import send_complaint_resolution_email
from accounts.decorators import student_required, staff_required, admin_required, staff_or_admin_required
from accounts.models import User

@student_required
def submit_complaint(request):
    """Allow students to submit new complaints"""
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        category = request.POST.get('category', '')
        priority = request.POST.get('priority', 'Medium')
        
        if not title or not description:
            messages.error(request, 'Please fill in all required fields (title and description)')
            return render(request, 'complaints/submit_complaint.html')
        
        try:
            # Create complaint
            complaint = Complaint.objects.create(
                title=title,
                description=description,
                category=category,
                priority=priority,
                user=request.user,
                student_id=request.user.id
            )
            
            # Process with AI classifier for department routing
            try:
                ComplaintClassifier.process_complaint(complaint)
                DepartmentRouter.assign_to_staff(complaint)

                if complaint.assigned_to:
                    messages.success(
                        request,
                        f'Complaint submitted successfully! Assigned to {complaint.assigned_to.get_full_name() or complaint.assigned_to.username} in {complaint.get_department_display()} department.'
                    )
                else:
                    messages.warning(
                        request,
                        f'Complaint submitted to {complaint.get_department_display()} department, but no staff available for assignment. It will be reviewed manually.'
                    )
            except Exception as e:
                import logging
                logger = logging.getLogger(__name__)
                logger.warning(f"AI processing failed for complaint {complaint.id}: {str(e)}")
                # If AI processing fails, just keep the complaint as is
                messages.info(request, 'Complaint submitted. Manual review required for department assignment.')

            # Create in-app notification for the user
            try:
                dept_display = complaint.get_department_display() if complaint.department else 'Unknown'
                Notification.objects.create(
                    user=request.user,
                    message=f'Your complaint "{complaint.title}" has been submitted and routed to {dept_display} department.',
                    complaint=complaint
                )
            except Exception as e:
                import logging
                logger = logging.getLogger(__name__)
                logger.warning(f"Failed to create notification for complaint {complaint.id}: {str(e)}")

            return redirect('my_complaints')
        except Exception as e:
            messages.error(request, f'Error creating complaint: {str(e)}')
            return render(request, 'complaints/submit_complaint.html')
    
    return render(request, 'complaints/submit_complaint.html')

@login_required(login_url='login')
def my_complaints(request):
    """Display user's submitted complaints with filtering"""
    if request.user.role == 'student':
        complaints = Complaint.objects.filter(user=request.user).order_by('-created_at')
    else:
        complaints = Complaint.objects.all().order_by('-created_at')
    
    # Get filter parameters
    search_query = request.GET.get('search', '').strip()
    status_filter = request.GET.get('status', '').strip()
    
    # Apply search filter
    if search_query:
        complaints = complaints.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    # Apply status filter
    if status_filter and status_filter in dict(Complaint.STATUS_CHOICES):
        complaints = complaints.filter(status=status_filter)
    
    context = {
        'complaints': complaints,
        'search_query': search_query,
        'status_filter': status_filter,
    }
    
    return render(request, 'complaints/complaint_list.html', context)

@login_required(login_url='login')
def complaint_detail(request, id):
    """Show detailed view of a specific complaint"""
    try:
        complaint = Complaint.objects.get(id=id)
        # Ensure user can only view their own complaints unless staff/HOD/admin
        if complaint.user != request.user and request.user.role not in ['staff', 'hod', 'admin']:
            messages.error(request, 'Unauthorized access')
            return redirect('my_complaints')
        
        # Get responses for this complaint
        responses = complaint.responses.all().order_by('-created_at')
        
        context = {
            'complaint': complaint,
            'responses': responses,
        }
        return render(request, 'complaints/complaint_detail.html', context)
    except Complaint.DoesNotExist:
        messages.error(request, 'Complaint not found')
        return redirect('my_complaints')

@staff_or_admin_required
def complaint_update(request, id):
    """Update complaint status (staff/admin only)"""
    try:
        complaint = Complaint.objects.get(id=id)
        
        if request.method == 'POST':
            try:
                status = request.POST.get('status', '').strip()
                response_text = request.POST.get('response', '').strip()
                
                if status not in dict(Complaint.STATUS_CHOICES):
                    messages.error(request, 'Invalid status provided')
                    return redirect('complaint_detail', id=complaint.id)
                
                complaint.status = status
                if request.user.role != 'admin':
                    complaint.assigned_to = request.user
                complaint.save()
                
                # Create response if provided
                if response_text:
                    try:
                        ComplaintResponse.objects.create(
                            complaint=complaint,
                            staff_member=request.user,
                            response=response_text
                        )
                    except Exception as e:
                        import logging
                        logger = logging.getLogger(__name__)
                        logger.error(f"Error creating complaint response: {str(e)}")
                        messages.warning(request, 'Complaint updated but response could not be saved')
                        return redirect('complaint_detail', id=complaint.id)
                
                # Send email and SMS notification if complaint is resolved or rejected
                if status in ('Resolved', 'Rejected'):
                    send_complaint_resolution_email(complaint, response_text)
                    from .sms_service import send_complaint_status_sms, send_high_priority_bulk_sms
                    try:
                        send_complaint_status_sms(complaint)
                        send_high_priority_bulk_sms(complaint)
                    except Exception:
                        pass
                
                messages.success(request, 'Complaint updated successfully!')
                return redirect('complaint_detail', id=complaint.id)
            except Exception as e:
                messages.error(request, f'Error updating complaint: {str(e)}')
                return redirect('complaint_detail', id=complaint.id)
        
        context = {
            'complaint': complaint,
            'status_choices': Complaint.STATUS_CHOICES,
        }
        return render(request, 'complaints/complaint_update.html', context)
    except Complaint.DoesNotExist:
        messages.error(request, 'Complaint not found')
        return redirect('assign_complaints')
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
        return redirect('assign_complaints')

@staff_or_admin_required
def assign_complaints(request):
    """Display complaints for staff assignment with filtering and department filtering"""
    # For staff, only show complaints from their department
    if request.user.role == 'staff':
        if request.user.department:
            complaints = Complaint.objects.filter(
                department=request.user.department
            ).order_by('-created_at')
        else:
            # Staff with no department assigned can see unassigned complaints
            complaints = Complaint.objects.filter(
                assigned_to__isnull=True
            ).order_by('-created_at')
    elif request.user.role == 'hod':
        # HOD sees all HOD-classified complaints
        complaints = Complaint.objects.filter(
            department='hod'
        ).order_by('-created_at')
    else:
        # Admins see all complaints
        complaints = Complaint.objects.all().order_by('-created_at')
    
    # Get filter parameters
    search_query = request.GET.get('search', '').strip()
    status_filter = request.GET.get('status', '').strip()
    assigned_filter = request.GET.get('assigned', '').strip()
    department_filter = request.GET.get('department', '').strip()
    
    # Apply search filter
    if search_query:
        complaints = complaints.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    # Apply status filter
    if status_filter and status_filter in dict(Complaint.STATUS_CHOICES):
        complaints = complaints.filter(status=status_filter)
    
    # Apply assignment filter
    if assigned_filter == 'unassigned':
        complaints = complaints.filter(assigned_to__isnull=True)
    elif assigned_filter == 'assigned':
        complaints = complaints.filter(assigned_to__isnull=False)
    
    # Apply department filter (admin only)
    if request.user.role == 'admin' and department_filter:
        if department_filter in dict(Complaint.DEPARTMENT_CHOICES):
            complaints = complaints.filter(department=department_filter)
    
    context = {
        'complaints': complaints,
        'search_query': search_query,
        'status_filter': status_filter,
        'assigned_filter': assigned_filter,
        'department_filter': department_filter,
        'user_department': request.user.department,
        'is_admin': request.user.role == 'admin',
        'department_choices': Complaint.DEPARTMENT_CHOICES,
    }
    
    return render(request, 'complaints/assign_complaints.html', context)

@admin_required
def complaints_stats(request):
    """Display complaint statistics with optional filtering (admin only)"""
    all_complaints = Complaint.objects.all()
    
    # Get filter parameters
    search_query = request.GET.get('search', '').strip()
    status_filter = request.GET.get('status', '').strip()
    
    # Apply search filter if provided
    filtered_complaints = all_complaints
    if search_query:
        filtered_complaints = filtered_complaints.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    # Apply status filter if provided
    if status_filter and status_filter in dict(Complaint.STATUS_CHOICES):
        filtered_complaints = filtered_complaints.filter(status=status_filter)
    
    # Use filtered complaints for stats unless no filter is applied
    complaints_for_stats = filtered_complaints if (search_query or status_filter) else all_complaints
    
    total = complaints_for_stats.count()
    pending = complaints_for_stats.filter(status='Pending').count()
    in_progress = complaints_for_stats.filter(status='In Progress').count()
    resolved = complaints_for_stats.filter(status='Resolved').count()
    rejected = complaints_for_stats.filter(status='Rejected').count()
    
    # Count by priority
    high_priority = complaints_for_stats.filter(priority='High').count()
    medium_priority = complaints_for_stats.filter(priority='Medium').count()
    low_priority = complaints_for_stats.filter(priority='Low').count()
    
    context = {
        'total': total,
        'pending': pending,
        'in_progress': in_progress,
        'resolved': resolved,
        'rejected': rejected,
        'high_priority': high_priority,
        'medium_priority': medium_priority,
        'low_priority': low_priority,
        'search_query': search_query,
        'status_filter': status_filter,
    }
    
    return render(request, 'complaints/complaint_stats.html', context)

@staff_or_admin_required
def staff_respond(request, id):
    """Staff member adds response to complaint"""
    try:
        complaint = Complaint.objects.get(id=id)
        
        if request.method == 'POST':
            response_text = request.POST.get('response', '').strip()
            if not response_text:
                messages.error(request, 'Response cannot be empty')
                return redirect('staff_respond', id=complaint.id)
            
            try:
                ComplaintResponse.objects.create(
                    complaint=complaint,
                    staff_member=request.user,
                    response=response_text
                )
                
                # Update complaint status if provided
                status = request.POST.get('status', '').strip()
                if status and status in dict(Complaint.STATUS_CHOICES):
                    complaint.status = status
                    # Only assign to staff member if they're in the correct department or if complaint is unassigned
                    if not complaint.assigned_to and request.user.department == complaint.department:
                        complaint.assigned_to = request.user
                        messages.info(request, 'Complaint has been assigned to you.')
                    elif complaint.assigned_to and complaint.assigned_to != request.user:
                        messages.warning(request, 'Cannot reassign complaint - already assigned to another staff member.')
                    complaint.save()
                    
                    # Send email and SMS notification if complaint is resolved or rejected
                    if status in ('Resolved', 'Rejected'):
                        send_complaint_resolution_email(complaint, response_text)
                        from .sms_service import send_complaint_status_sms, send_high_priority_bulk_sms
                        try:
                            send_complaint_status_sms(complaint)
                            send_high_priority_bulk_sms(complaint)
                        except Exception:
                            pass
                
                messages.success(request, 'Response added successfully!')
                return redirect('complaint_detail', id=complaint.id)
            except Exception as e:
                messages.error(request, f'Error adding response: {str(e)}')
                return redirect('staff_respond', id=complaint.id)
        
        responses = complaint.responses.all().order_by('-created_at')
        context = {
            'complaint': complaint,
            'responses': responses,
            'status_choices': Complaint.STATUS_CHOICES,
        }
        return render(request, 'complaints/staff_response.html', context)
    except Complaint.DoesNotExist:
        messages.error(request, 'Complaint not found')
        return redirect('assign_complaints')
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
        return redirect('assign_complaints')


@student_required
def delete_complaint(request, id):
    """Delete a complaint (students can only delete their own pending complaints)"""
    try:
        complaint = Complaint.objects.get(id=id)
        
        # Verify ownership
        if complaint.user != request.user:
            messages.error(request, 'You can only delete your own complaints')
            return redirect('my_complaints')
        
        # Only allow deletion of pending complaints
        if complaint.status != 'Pending':
            messages.error(request, 'You can only delete pending complaints')
            return redirect('complaint_detail', id=complaint.id)
        
        complaint_title = complaint.title
        
        # Delete associated responses first (cascade delete)
        try:
            complaint.responses.all().delete()
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Error deleting complaint responses: {str(e)}")
        
        # Delete the complaint
        complaint.delete()
        messages.success(request, f'Complaint "{complaint_title}" has been deleted successfully!')
        return redirect('my_complaints')
        
    except Complaint.DoesNotExist:
        messages.error(request, 'Complaint not found')
        return redirect('my_complaints')
    except Exception as e:
        messages.error(request, f'Error deleting complaint: {str(e)}')
        return redirect('my_complaints')
