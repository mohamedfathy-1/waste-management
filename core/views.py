from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q, Count
from accounts.decorators import citizen_required, staff_required, admin_required
from accounts.models import User
from .models import RecyclingCenter, WasteReport
from .forms import WasteReportForm, ReportStatusForm, RecyclingCenterForm, UserRoleForm
import math
import json


# Home view
def home(request):
    """Landing page that redirects based on authentication"""
    if request.user.is_authenticated:
        if request.user.is_admin_user():
            return redirect('admin_dashboard')
        elif request.user.is_staff_user():
            return redirect('staff_dashboard')
        else:
            return redirect('citizen_dashboard')
    return redirect('login')


# ===================================
# CITIZEN VIEWS
# ===================================

@citizen_required
def citizen_dashboard(request):
    """Citizen dashboard showing their reports summary"""
    reports = WasteReport.objects.filter(citizen=request.user)
    
    recent_reports = reports.order_by('-created_at')[:5]
    
    context = {
        'total_reports': reports.count(),
        'pending_reports': reports.filter(status='pending').count(),
        'in_progress_reports': reports.filter(status='in_progress').count(),
        'completed_reports': reports.filter(status='completed').count(),
        'recent_reports': recent_reports,
    }
    return render(request, 'citizen/dashboard.html', context)


@citizen_required
def submit_report(request):
    """Submit a new waste report"""
    if request.method == 'POST':
        form = WasteReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.citizen = request.user
            
            # Try to assign to nearest recycling center
            latitude = float(form.cleaned_data['latitude'])
            longitude = float(form.cleaned_data['longitude'])
            center = find_nearest_center(latitude, longitude)
            if center:
                report.center = center
            
            report.save()
            messages.success(request, 'Your waste report has been submitted successfully!')
            return redirect('track_reports')
    else:
        form = WasteReportForm()
    
    return render(request, 'citizen/submit_report.html', {'form': form})


@citizen_required
def track_reports(request):
    """Track all reports submitted by the citizen"""
    reports = WasteReport.objects.filter(citizen=request.user).select_related('center')
    return render(request, 'citizen/track_reports.html', {'reports': reports})


@citizen_required
def map_centers(request):
    """Display all recycling centers on a map"""
    centers = RecyclingCenter.objects.all()
    
    # Serialize centers data for JavaScript
    centers_data = []
    for center in centers:
        centers_data.append({
            'id': center.id,
            'name': center.name,
            'address': center.address,
            'latitude': float(center.latitude),
            'longitude': float(center.longitude),
            'materials_accepted': center.materials_accepted,
            'working_hours': center.working_hours,
        })
    
    context = {
        'centers': centers,
        'centers_json': json.dumps(centers_data),
    }
    
    return render(request, 'citizen/map_centers.html', context)


@citizen_required
def center_detail(request, pk):
    """Display details of a specific recycling center"""
    center = get_object_or_404(RecyclingCenter, pk=pk)
    return render(request, 'citizen/center_detail.html', {'center': center})


# ===================================
# STAFF VIEWS
# ===================================

@staff_required
def staff_dashboard(request):
    """Staff dashboard showing assigned reports"""
    try:
        center = request.user.assigned_center.get()
        reports = WasteReport.objects.filter(center=center).select_related('citizen')
        
        recent_reports = reports.order_by('-created_at')[:10]
        
        context = {
            'center': center,
            'total_reports': reports.count(),
            'pending_reports': reports.filter(status='pending').count(),
            'in_progress_reports': reports.filter(status='in_progress').count(),
            'completed_reports': reports.filter(status='completed').count(),
            'recent_reports': recent_reports,
        }
    except RecyclingCenter.DoesNotExist:
        context = {
            'center': None,
            'total_reports': 0,
            'pending_reports': 0,
            'in_progress_reports': 0,
            'completed_reports': 0,
            'recent_reports': [],
        }
        messages.warning(request, 'You are not assigned to any recycling center yet.')
    
    return render(request, 'staff/dashboard.html', context)


@staff_required
def view_reports(request):
    """View all reports assigned to staff's center"""
    try:
        center = request.user.assigned_center.get()
        reports = WasteReport.objects.filter(center=center).select_related('citizen')
        
        # Filter by status if provided
        status_filter = request.GET.get('status')
        if status_filter:
            reports = reports.filter(status=status_filter)
        
        context = {
            'center': center,
            'reports': reports,
            'status_filter': status_filter,
        }
    except RecyclingCenter.DoesNotExist:
        context = {
            'center': None,
            'reports': [],
        }
        messages.warning(request, 'You are not assigned to any recycling center yet.')
    
    return render(request, 'staff/view_reports.html', context)


@staff_required
def update_report_status(request, pk):
    """Update the status of a report"""
    report = get_object_or_404(WasteReport, pk=pk)
    
    # Verify staff can only update reports assigned to their center
    try:
        center = request.user.assigned_center.get()
        if report.center != center:
            messages.error(request, 'You can only update reports assigned to your center.')
            return redirect('view_reports')
    except RecyclingCenter.DoesNotExist:
        messages.error(request, 'You are not assigned to any recycling center.')
        return redirect('staff_dashboard')
    
    if request.method == 'POST':
        form = ReportStatusForm(request.POST, instance=report)
        if form.is_valid():
            form.save()
            messages.success(request, 'Report status updated successfully!')
            return redirect('view_reports')
    else:
        form = ReportStatusForm(instance=report)
    
    return render(request, 'staff/update_status.html', {'form': form, 'report': report})


@staff_required
def update_center_info(request):
    """Update recycling center information"""
    try:
        center = request.user.assigned_center.get()
    except RecyclingCenter.DoesNotExist:
        messages.error(request, 'You are not assigned to any recycling center.')
        return redirect('staff_dashboard')
    
    if request.method == 'POST':
        form = RecyclingCenterForm(request.POST, instance=center)
        if form.is_valid():
            form.save()
            messages.success(request, 'Center information updated successfully!')
            return redirect('staff_dashboard')
    else:
        form = RecyclingCenterForm(instance=center)
    
    return render(request, 'staff/update_center.html', {'form': form, 'center': center})


# ===================================
# ADMIN VIEWS
# ===================================

@admin_required
def admin_dashboard(request):
    """Admin dashboard with statistics"""
    stats = {
        'total_reports': WasteReport.objects.count(),
        'pending': WasteReport.objects.filter(status='pending').count(),
        'in_progress': WasteReport.objects.filter(status='in_progress').count(),
        'completed': WasteReport.objects.filter(status='completed').count(),
        'total_centers': RecyclingCenter.objects.count(),
        'total_users': User.objects.count(),
        'total_citizens': User.objects.filter(role='citizen').count(),
        'total_staff': User.objects.filter(role='staff').count(),
    }
    
    recent_reports = WasteReport.objects.select_related('citizen', 'center')[:10]
    
    context = {
        'stats': stats,
        'recent_reports': recent_reports,
    }
    return render(request, 'admin_panel/dashboard.html', context)


@admin_required
def manage_reports(request):
    """Manage all waste reports"""
    reports = WasteReport.objects.select_related('citizen', 'center')
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        reports = reports.filter(status=status_filter)
    
    # Search
    search_query = request.GET.get('search')
    if search_query:
        reports = reports.filter(
            Q(citizen__username__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    context = {
        'reports': reports,
        'status_filter': status_filter,
        'search_query': search_query,
    }
    return render(request, 'admin_panel/manage_reports.html', context)


@admin_required
def delete_report(request, pk):
    """Delete a waste report"""
    report = get_object_or_404(WasteReport, pk=pk)
    report.delete()
    messages.success(request, 'Report deleted successfully!')
    return redirect('manage_reports')


@admin_required
def manage_centers(request):
    """Manage all recycling centers"""
    centers = RecyclingCenter.objects.select_related('assigned_staff')
    
    # Search
    search_query = request.GET.get('search')
    if search_query:
        centers = centers.filter(
            Q(name__icontains=search_query) |
            Q(address__icontains=search_query)
        )
    
    context = {
        'centers': centers,
        'search_query': search_query,
    }
    return render(request, 'admin_panel/manage_centers.html', context)


@admin_required
def add_center(request):
    """Add a new recycling center"""
    if request.method == 'POST':
        form = RecyclingCenterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Recycling center added successfully!')
            return redirect('manage_centers')
    else:
        form = RecyclingCenterForm()
    
    return render(request, 'admin_panel/add_center.html', {'form': form})


@admin_required
def edit_center(request, pk):
    """Edit a recycling center"""
    center = get_object_or_404(RecyclingCenter, pk=pk)
    
    if request.method == 'POST':
        form = RecyclingCenterForm(request.POST, instance=center)
        if form.is_valid():
            form.save()
            messages.success(request, 'Recycling center updated successfully!')
            return redirect('manage_centers')
    else:
        form = RecyclingCenterForm(instance=center)
    
    return render(request, 'admin_panel/edit_center.html', {'form': form, 'center': center})


@admin_required
def delete_center(request, pk):
    """Delete a recycling center"""
    center = get_object_or_404(RecyclingCenter, pk=pk)
    center.delete()
    messages.success(request, 'Recycling center deleted successfully!')
    return redirect('manage_centers')


@admin_required
def manage_users(request):
    """Manage all users"""
    users = User.objects.all()
    
    # Filter by role
    role_filter = request.GET.get('role')
    if role_filter:
        users = users.filter(role=role_filter)
    
    # Search
    search_query = request.GET.get('search')
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query)
        )
    
    context = {
        'users': users,
        'role_filter': role_filter,
        'search_query': search_query,
    }
    return render(request, 'admin_panel/manage_users.html', context)


@admin_required
def assign_role(request, pk):
    """Assign or change user role"""
    user = get_object_or_404(User, pk=pk)
    
    if request.method == 'POST':
        form = UserRoleForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Role updated for {user.username}!')
            return redirect('manage_users')
    else:
        form = UserRoleForm(instance=user)
    
    return render(request, 'admin_panel/assign_role.html', {'form': form, 'user': user})


@admin_required
def statistics_api(request):
    """API endpoint for dashboard statistics"""
    # Reports by status
    status_stats = {
        'pending': WasteReport.objects.filter(status='pending').count(),
        'in_progress': WasteReport.objects.filter(status='in_progress').count(),
        'completed': WasteReport.objects.filter(status='completed').count(),
    }
    
    # Reports by area (simplified - grouping by center)
    area_stats = []
    centers = RecyclingCenter.objects.annotate(report_count=Count('reports'))
    for center in centers:
        area_stats.append({
            'name': center.name,
            'count': center.report_count,
        })
    
    data = {
        'status_stats': status_stats,
        'area_stats': area_stats,
    }
    
    return JsonResponse(data)


# ===================================
# UTILITY FUNCTIONS
# ===================================

def find_nearest_center(latitude, longitude):
    """Find the nearest recycling center using Haversine formula"""
    centers = RecyclingCenter.objects.all()
    
    if not centers:
        return None
    
    min_distance = float('inf')
    nearest_center = None
    
    for center in centers:
        distance = calculate_distance(
            latitude, longitude,
            float(center.latitude), float(center.longitude)
        )
        if distance < min_distance:
            min_distance = distance
            nearest_center = center
    
    return nearest_center


def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two points using Haversine formula"""
    R = 6371  # Earth's radius in kilometers
    
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    
    return distance
