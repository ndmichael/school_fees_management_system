from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from fees.models import Student, Payment, Staff, Course, Complaint
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import PaymentProofForm, ComplaintForm
from fees.forms import PaymentFilterForm
from django.http import HttpResponseForbidden

# Create your views here.


@login_required
def payment_proof(request):
    '''Manage Payment proof here'''

    if not hasattr(request.user, 'student_user'):
        messages.error(
                    request, f"You do not exist as a student"
                )
        return redirect(
            "account_login"
        ) 

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