from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def staff_required(view_func):
    @login_required # Redirect to login page if not logged in
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(request, "You do not have permission to access this page.")
            return redirect("/")
        return view_func(request, *args, **kwargs)
    return wrapper
