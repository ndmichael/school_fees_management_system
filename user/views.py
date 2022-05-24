from django.shortcuts import render
from fees.models import Student, Payment

# Create your views here.


def student_profile(request, username):
    student = Student.objects.filter(user__username=username).first()
    payments = Payment.objects.filter(student=student)
    context = {
        'student': student,
        'payments': payments
    }
    return render(request, 'account/student_profile.html', context)
