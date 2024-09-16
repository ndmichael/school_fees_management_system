from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from fees.models import Student, Payment, Staff, Course
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import PaymentProofForm

# Create your views here.


@login_required
def payment_proof(request):
    '''Manage Payment proof here'''

    if request.POST:
        form = PaymentProofForm(request.POST, request.FILES)

        if form.is_valid():
            pp_form = form.save(commit=False)

            student = get_object_or_404(
                Student,
                user = request.user
            ) 

            if student:
                pp_form.student = student
                pp_form.save()
                messages.success(
                    request, f"Payment proof has been submitted"
                )
            else:
                messages.danger(
                    request, f"User doesn't exist"
                )

            
        return redirect(
                    "payment_proof"
                )   
             
            
        
    form = PaymentProofForm
    context = {
        'pp_form': form
    }
    return render(request, 'students/payment_proof.html',context)
