from django.shortcuts import render, redirect
from fees.models import Student, Payment
from fees.forms import RemarkForm
from django.contrib import messages

# Create your views here.


def student_profile(request, username):
    if request.POST:
        r_form = RemarkForm(request.POST, instance=request.user)
        if r_form.is_valid():
            r_form.save(commit=False)
            r_form.user = request.user
            r_form.save()
            messages.success(request, f"Message Has Been Sent.")
            return redirect(
                "stud_profile", username=request.user.username
            ) 

    student = Student.objects.filter(user__username=username).first()
    payments = Payment.objects.filter(student=student)

    r_form = RemarkForm()
    context = {
        'student': student,
        'payments': payments,
        'r_form': r_form
    }
    return render(request, 'account/student_profile.html', context)


