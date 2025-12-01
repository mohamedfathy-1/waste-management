from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def citizen_required(view_func):
    """Decorator to restrict access to citizen users only"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to access this page.')
            return redirect('login')
        if not request.user.is_citizen():
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper


def staff_required(view_func):
    """Decorator to restrict access to staff users only"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to access this page.')
            return redirect('login')
        if not request.user.is_staff_user():
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper


def admin_required(view_func):
    """Decorator to restrict access to admin users only"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to access this page.')
            return redirect('login')
        if not request.user.is_admin_user():
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper
