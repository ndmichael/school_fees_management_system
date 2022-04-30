from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import StaffProfile, StudentProfile

class UserForm(UserCreationForm):
    email = forms.EmailField()
    username = forms.CharField()
    username.help_text = ''
    class Meta:
        model = User
        fields = ['username','email', 'first_name', 'last_name', 'password1', 'password2']


class StudentForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        widgets = {
          'address': forms.Textarea(attrs={'rows':2})
        }
        fields =  ['faculty', 'courses', 'address', 'gender', 'admission_date']

class AdminForm(forms.ModelForm):
    pass
    
