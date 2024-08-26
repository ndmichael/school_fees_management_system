from allauth.account.forms import SignupForm, LoginForm
from django import forms
from django.contrib.auth.models import User
from fees.models import Staff

class SelfLoginForm (LoginForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["login"].widget.attrs.update(
            {'class': 'form-control-lg rounded-4  mb-4'})
        self.fields["password"].widget.attrs.update(
            {'class': 'form-control-lg rounded-4 mb-4 '})
        

class UserUpdateForm(forms.ModelForm):
    """Form to update staff as user."""
    class Meta:
        model = User
        fields = ['last_name', 'first_name', 'username', 'email']


class StudentUpdateForm(forms.ModelForm):
    """Form to update staff profile."""
    class Meta:
        model = Staff
        fields = ['image', 'mobileNo', 'dob', 'Address']