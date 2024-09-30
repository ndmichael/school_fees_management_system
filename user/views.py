from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from fees.models import Student, Payment, Staff, Course
from .forms import UserUpdateForm, StaffUpdateForm, ProfilePicUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.db.models import Sum
from  nile.decorators import staff_required

# Create your views here.


# def stud_profile(request, username):
#     '''*** Student profile section 1 ***
#         === All logics goes her ===
#     '''
    
#     if request.POST:
#         r_form = ComplaintForm(request.POST)
#         if r_form.is_valid():
#             form = r_form.save(commit=False)
#             form.student = request.user.student_user
#             r_form.save()
#             messages.success(request, f"Message Has Been Sent.")
#             return redirect(
#                 "stud_profile", username=request.user.username
#             ) 
#     else:
#         r_form = ComplaintForm()

#     student = Student.objects.filter(user__username=username).first()
#     payments = Payment.objects.filter(student=student)

#     context = {
#         'student': student,
#         'payments': payments,
#         'r_form': r_form,
#         "title": "profile page"
#     }
#     return render(request, 'account/stud_profile.html', context)

@login_required
def staff_profile(request, username):
    '''*** Staff profile section ***'''

    user = User.objects.get(username=username)
    staff = Staff.objects.filter(user=user).first()
    payments_handled_by_staff = Payment.objects.filter(staff=staff)
    total_payments_handled_by_staff = payments_handled_by_staff.count()
    total_amount_handled_by_staff = payments_handled_by_staff.aggregate(total=Sum('amount'))['total']

    if request.POST:
        userUpdateForm = UserUpdateForm(request.POST, instance=user)
        staffUpdateForm = StaffUpdateForm(
            request.POST,
            request.FILES,
            instance=staff 
        )
        if userUpdateForm.is_valid() and staffUpdateForm.is_valid():
            userUpdateForm.save()
            staffUpdateForm.save()
            messages.success(
                    request, f"Profile Updated successfully."
                )
            return redirect("staff_profile", user.username)

    else:
        userUpdateForm = UserUpdateForm(instance=user)
        staffUpdateForm = StaffUpdateForm(
            instance=staff 
        )

        

    context = {
        'staff': staff,
        "title": "staff profile",
        "total_payments": total_payments_handled_by_staff,
        "total_amounts": total_amount_handled_by_staff,
        "userUpdateForm": userUpdateForm,
        "staffUpdateForm": staffUpdateForm
    }
    return render(request, 'account/staff_profile.html', context)


@login_required
def current_user_dashboard(request):
    '''On login if admin ? redirect admin dashboard else student profile'''

    if request.user.is_staff:
        return redirect('admin_dashboard')
    return redirect('student_dashboard')


@login_required
@staff_required
def user_settings(request):
    update_image_form = ProfilePicUpdateForm
    if request.POST:
        update_image = ProfilePicUpdateForm(request.POST, request.FILES)
        if update_image.is_valid():
            staff = Staff.objects.get(user=request.user)
            staff.image = update_image.cleaned_data['profile_pic']
            staff.save()
            messages.success(
                    request, f"Profile Image updated successfully."
                )
            return redirect("user_settings")
    context = {
        'update_image_form': update_image_form
    }
    return render(request, 'account/user_settings.html', context)