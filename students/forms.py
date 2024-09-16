from django import forms
from django.contrib.auth.models import User
from fees.models import Student, Payment, Complaint


class PaymentProofForm(forms.ModelForm):
    """Form to update payment"""
    class Meta:
        model = Payment
        fields = ['academic_year', 'semester', 'amount', 'payment_method', 'image']