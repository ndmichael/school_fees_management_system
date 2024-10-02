from django import forms
from django.contrib.auth.models import User
from fees.models import Student, Payment, Complaint
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Div
from crispy_bootstrap5.bootstrap5 import FloatingField, Field


class PaymentProofForm(forms.ModelForm):
    """Form to update payment"""
    class Meta:
        model = Payment
        fields = [
            'academic_year', 
            'semester', 
            'amount', 
            'payment_method', 
            'reference_number',
            'image'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = True
        self.helper = FormHelper()
        # self.helper.disable_csrf = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                FloatingField("academic_year", wrapper_class='col-md-6'),
                FloatingField("semester", wrapper_class='col-md-6'),
                FloatingField("amount", wrapper_class='col-md-6'),
                FloatingField("payment_method", wrapper_class='col-md-6'),
                FloatingField("reference_number", wrapper_class='col-md-12'),
                FloatingField("image", wrapper_class='col-md-12'),
                Div(
                    Submit('submit', 'SEND PROOF', css_class='btn-lg col-12 px-2')
                )
                
            ),
        )


class ComplaintForm(forms.ModelForm):

    class Meta:
        model = Complaint
        fields = ['subject', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subject'].widget.attrs.update({
            'class': 'form-control form-control-lg mb-0',
            'placeholder': 'Subject of complain',
        })

        self.fields['description'].widget.attrs.update({
            'placeholder': 'Describe your complains',
            'rows': 4
        })



class StudentUpdateForm(forms.ModelForm):
    """Form to update student profile."""
    class Meta:
        model = Student
        fields = ['mobile_number', 'dob', 'address']

    def __init__(self, *args, **kwargs):
        super(StudentUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                FloatingField("mobile_number", wrapper_class='col-md-6'),
                FloatingField("dob", wrapper_class='col-md-6'),
            ),
            Row(
                Field("address", rows=6, wrapper_class='col-12'),
            )  
        )