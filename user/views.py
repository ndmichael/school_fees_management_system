from django.shortcuts import render, redirect
from fees.models import Student, Payment
from fees.forms import RemarkForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.


def stud_profile(request, username):
    if request.POST:
        r_form = RemarkForm(request.POST)
        if r_form.is_valid():
            form = r_form.save(commit=False)
            form.student = request.user.student_user
            r_form.save()
            messages.success(request, f"Message Has Been Sent.")
            return redirect(
                "stud_profile", username=request.user.username
            ) 
    else:
        r_form = RemarkForm()

    student = Student.objects.filter(user__username=username).first()
    payments = Payment.objects.filter(student=student)

    
    context = {
        'student': student,
        'payments': payments,
        'r_form': r_form,
        "title": "profile page"
    }
    return render(request, 'account/stud_profile.html', context)


@login_required
def student_profile(request, username):
    print("username : ", username)
    student = Student.objects.filter(user__username=username).first()
    payments = Payment.objects.filter(student=student)
    context = {
        'student': student,
        'payments': payments,
        "title": "student profile"
    }
    return render(request, 'account/student_profile.html', context)

