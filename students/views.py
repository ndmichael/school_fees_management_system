from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from fees.models import Student, Payment, Staff, Course
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import PaymentProofForm
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
    payments = Payment.objects.all()
    context = {
        'payments': payments,
    }
    return render(request, 'students/make_payment.html',context)