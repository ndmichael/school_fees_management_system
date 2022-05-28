from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm , UsernameField
from .models import Staff, Student, Payment, Remark

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
    class Meta:
        model = Student
        widgets = {
          'address': forms.Textarea(attrs={'rows':2})
        }
        fields =  ['faculty', 'courses','mobile_number', 'address', 'gender', 'admission_date', 'image']


class RemarkForm(forms.ModelForm):
    class Meta:
        model = Remark
        widgets = {
          'body': forms.Textarea(attrs={'rows':4})
        }
        fields = ['subject', 'body']
    

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['last_name', 'first_name', 'username']


class StudentUpdateForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['image', 'faculty', 'courses', 'address', 'mobile_number']


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['student','academic_year', 'semester', 'amount', 'payment_method']

class PaymentUpdateForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['student','academic_year', 'semester', 'amount', 'payment_method']

class DeactivateStudent(forms.Form):
    deactivate = forms.BooleanField()

class AdminForm(forms.ModelForm):
    pass
    
