from django.shortcuts import render, redirect
from fees.models import Student, Payment, Staff, Course
from fees.forms import ComplaintForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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
def student_profile(request, username):
    '''*** Student profile section ***
        === All logics goes her ===
    '''

    student = Student.objects.filter(user__username=username).first()
    payments = Payment.objects.filter(student=student)

    context = {
        'student': student,
        'payments': payments,
        "title": "student profile"
    }
    return render(request, 'account/student_profile.html', context)

@login_required
def staff_profile(request, username):
    '''*** Staff profile section ***'''

    print("username : ", username)
    staff = Staff.objects.filter(user__username=username).first()
    context = {
        'staff': staff,
        "title": "staff profile"
    }
    return render(request, 'account/staff_profile.html', context)


@login_required
def current_user_profile(request):
    '''On login if admin ? redirect admin dashboard else student profile'''

    if request.user.is_staff:
        return redirect('admin_dashboard')
    return redirect('student_profile', username=request.user.username)