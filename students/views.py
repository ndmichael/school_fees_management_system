from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from fees.models import Student, Payment, Staff, Course, Complaint
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import PaymentProofForm, ComplaintForm, StudentUpdateForm
from fees.forms import PaymentFilterForm
from user.forms import UserUpdateForm
from django.http import HttpResponseForbidden
from nile.decorators import student_required

# Create your views here.

@login_required
@student_required
def student_dashboard(request):
    '''*** Student Dashboard section ***
        === All logics goes her ===
    '''
    student = Student.objects.filter(user=request.user).first()
    payments = Payment.objects.filter(student=student).order_by('-date_entered')

    context = {
        'student': student,
        'payments': payments,
        "title": "student profile"
    }
    return render(request, 'students/student_dashboard.html', context)


@login_required
def student_profile(request, username):
    '''*** Student profile section ***
        === All logics goes her ===
    '''
    user = User.objects.get(username=username)
    student = Student.objects.get(user=user)
    payments = Payment.objects.filter(student=student).order_by('-date_entered')
    total_successful_payment = Payment.objects.filter(student=student, status="confirmed").count()
    total_pending_payment = Payment.objects.filter(student=student, status="pending").count()
    total_payment = payments.count()

    if request.POST:
        userUpdateForm = UserUpdateForm(request.POST, instance=user)
        studentUpdateForm = StudentUpdateForm(
            request.POST,
            request.FILES,
            instance=student 
        )
        if userUpdateForm.is_valid() and studentUpdateForm.is_valid():
            userUpdateForm.save()
            studentUpdateForm.save()
            messages.success(
                    request, f"Profile Updated successfully."
                )
            return redirect("student_profile", user.username)

    else:
        userUpdateForm = UserUpdateForm(instance=user)
        studentUpdateForm = StudentUpdateForm(
            instance=student
        )

    context = {
        'student': student,
        'payments': payments,
        "total_pending_payment": total_pending_payment,
        "total_successful_payment": total_successful_payment,
        'total_payment': total_payment,
        "title": "student profile",
        "userUpdateForm": userUpdateForm,
        "studentUpdateForm": studentUpdateForm,
    }
    return render(request, 'students/student_profile.html', context)


@login_required
@student_required
def payment_proof(request):
    '''Manage Payment proof here'''

    if request.method == 'POST':
        form = PaymentProofForm(request.POST, request.FILES)

        if form.is_valid():
            pp_form = form.save(commit=False)

            student = get_object_or_404(
                Student,
                user = request.user
            ) 
            pp_form.student = student
            pp_form.save()
            messages.success(
                request, f"Payment proof has been submitted"
            )
               
        return redirect(
            "payment_proof"
        )   
    else:
        form = PaymentProofForm()

    context = {
        'pp_form': form
    }
    return render(request, 'students/payment_proof.html',context)


@login_required
@student_required
def make_payment(request):
    student = Student.objects.get(user=request.user)
    payments = Payment.objects.filter(student=student).order_by('-date_entered')

    paymentFilterForm =  PaymentFilterForm
    # if get_payment_id and get_payment_id != '':
    #    payments = Payment.objects.annotate(search=SearchVector('id'),).filter(search__icontains=get_payment_id)
    # if get_start_date and get_start_date != '':
    #     payments = Payment.objects.annotate(search=SearchVector('id'),).filter(search__gte=get_payment_id)
    # if get_end_date and get_end_date != '':
    #     payments = Payment.objects.annotate(search=SearchVector('id'),).filter(search__lt=get_payment_id)

    context = {
        'payments': payments,
        'paymentFilterForm': paymentFilterForm,
    }
    return render(request, 'students/make_payment.html',context)


@login_required
@student_required
def payment_complaints(request):
    student = Student.objects.get(user=request.user)
    complaints = Complaint.objects.filter(student = student).order_by('-date_submitted')
    if request.method == "POST":
        complaintForm = ComplaintForm(request.POST)
        if complaintForm.is_valid():
            c_form = complaintForm.save(commit=False)
            c_form.student = student
            c_form.save()
            messages.success(
                request, f"Complaint sent, await response"
            )
            return redirect(
                "payment_complaints"
            ) 
    else:
        complaintForm = ComplaintForm()
    context = {
        "complaintForm": complaintForm,
        "complaints": complaints,
    }
    return render(request, 'students/payment_complaints.html',context)