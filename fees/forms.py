from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm , UsernameField
from .models import Staff, Student, Payment, Complaint
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Row
from crispy_bootstrap5.bootstrap5 import FloatingField


sems = (
        ('semester 1', 'SEMESTER 1'),
        ('semester 2', 'SEMESTER 2')
    )

class UserForm(UserCreationForm):
    email = forms.EmailField()
    username = forms.CharField()
    username = UsernameField(
        label='User ID',
        widget=forms.TextInput(attrs={'autofocus': True})
    )
    class Meta:
        model = User
        fields = ['username','email', 'first_name', 'last_name', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
            super(UserForm, self).__init__(*args, **kwargs)

            for fieldname in ['username', 'password1', 'password2']:
                self.fields[fieldname].help_text = None


class DateInput(forms.DateInput):
    input_type = 'date'

class StudentForm(forms.ModelForm):
    admission_date = forms.DateField(widget=DateInput)
    dob = forms.DateField(widget=DateInput)
    class Meta:
        model = Student
        widgets = {
          'address': forms.Textarea(attrs={'rows':2})
        }
        fields =  ['faculty', 'courses','mobile_number', 'address', 'gender','dob', 'admission_date', 'image']


class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        widgets = {
          'body': forms.Textarea(attrs={'rows':4})
        }
        fields = ['subject', 'description']
    

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['last_name', 'first_name', 'username']


class StudentUpdateForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['image', 'faculty', 'courses', 'address', 'mobile_number']


class PaymentForm(forms.ModelForm):
    date_paid = forms.DateField(widget=DateInput)
    class Meta:
        model = Payment
        fields = ['student','academic_year', 'semester', 'amount', 'payment_method', 'date_paid']

class PaymentUpdateForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['student','academic_year', 'semester', 'amount', 'payment_method']


# class OnlinePaymentForm(forms.Form):
#     cardnumber = forms.CharField(max_length=16)
#     cvc = forms.IntegerField()
#     expiration_date =forms.DateField()
#     academic_year = forms.CharField(max_length=4)
#     semester = forms.CharField(choices=sems)
#     amount = forms.DecimalField(max_digits=10, decimal_places=2)


class DeactivateStudent(forms.Form):
    deactivate = forms.BooleanField()
    

class AdminForm(forms.ModelForm):
    pass


# search feature for payment
class PaymentSearchForm(forms.Form):
    query = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['query'].label = ''
        self.fields['query'].widget.attrs.update({
            'class': 'form-control form-control-lg mb-0',
            'placeholder': 'Search payments by payment id, academic year...',
    })
        
class StudentSearchForm(forms.Form):
    query = forms.CharField(
        required=False, 
        widget=forms.TextInput(attrs={'required': 'false'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['query'].label = ''
        self.fields['query'].widget.attrs.update({
            'class': 'form-control form-control-lg mb-0',
            'placeholder': 'Search by student name, student id',
    })
        

class ComplaintFilterForm(forms.Form):
    STATUS  =( 
        ('', '----'),
        ('P', 'Pending'),
        ('R', 'Resolved'),
        ('C', 'Closed')
    )
    reference_id = forms.CharField()
    status = forms.ChoiceField(choices=STATUS, required=False)

    def __init__(self, *args, **kwargs):
        super(ComplaintFilterForm, self).__init__(*args, **kwargs)
        # super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                FloatingField("reference_id", wrapper_class='col-md-4'),
                FloatingField("status", wrapper_class='col-md-4'),
                Div(
                    Submit('submit', 'filter',  css_class="col-12 col-md-8 btn-danger h-75"), 
                    css_class='col-md-4',
                    
                )
                
            ),
        )

    
