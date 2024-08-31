from allauth.account.forms import SignupForm, LoginForm
from django import forms
from django.contrib.auth.models import User
from fees.models import Staff

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Row
from crispy_bootstrap5.bootstrap5 import FloatingField, Field

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].disabled = True
        self.fields['email'].disabled = True
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                FloatingField("username", wrapper_class='col-md-6'),
                FloatingField("email", wrapper_class='col-md-6'),
                FloatingField("last_name", wrapper_class='col-md-6'),
                FloatingField("first_name", wrapper_class='col-md-6'),
            ),
        )


class StaffUpdateForm(forms.ModelForm):
    """Form to update staff profile."""
    class Meta:
        model = Staff
        fields = ['image', 'mobileNo', 'DOB', 'address']

    def __init__(self, *args, **kwargs):
        super(StaffUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                FloatingField("mobileNo", wrapper_class='col-md-6'),
                FloatingField("DOB", wrapper_class='col-md-6'),
            ),
            Row(
                Field("address", rows=6, wrapper_class='col-12'),
            )  
        )


class ProfilePicUpdateForm(forms.Form):
    profile_pic = forms.FileField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profile_pic'].widget.attrs.update({
            'class': 'form-control form-control-lg mb-0',
         })