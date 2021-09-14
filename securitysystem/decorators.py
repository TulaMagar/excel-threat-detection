"""
Module for decorator permissions for views
"""

from django.shortcuts import redirect
from django.shortcuts import render

def unauthenticated_user(view_func):
    """
    Checks whether a user is authenticated or not
    """
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

def allowed_users(allowed_roles=[]):
    """
    Checks if a user is part of the allowed roles group for the page
    """
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return render(request, 'bad_role.html')
        return wrapper_func
    return decorator
