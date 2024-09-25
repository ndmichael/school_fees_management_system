from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def staff_required(view_func):
    @login_required # Redirect to login page if not logged in
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(request, "You do not have permission to access this page.")
            return redirect("account_login")
        return view_func(request, *args, **kwargs)
    return wrapper


def student_required(view_func):
    @login_required(login_url='account_login')  # Redirect to login if not logged in
    def wrapper(request, *args, **kwargs):
        if not hasattr(request.user, 'student_user'):
            messages.error(request, "You do not exist as a student.")
            return redirect("account_login")
        return view_func(request, *args, **kwargs)
    return wrapper
