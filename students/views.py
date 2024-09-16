from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from fees.models import Student, Payment, Staff, Course
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import PaymentProofForm

# Create your views here.


@login_required
def payment_proof(request):
    '''Manage Payment proof here'''
    form = PaymentProofForm
    context = {
        'pp_form': form
    }
    return render(request, 'students/payment_proof.html',context)
