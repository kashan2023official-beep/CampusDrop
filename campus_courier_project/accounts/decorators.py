from functools import wraps
from django.contrib import messages
from django.shortcuts import redirect


def courier_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not getattr(request.user, 'profile', None) or not request.user.profile.is_courier:
            messages.error(request, "Switch to courier mode first.")
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper


def staff_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_staff:
            messages.error(request, "Staff access required.")
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper
