from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm , UsernameField
from .models import Student, Payment, Complaint
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Row, BaseInput
from crispy_bootstrap5.bootstrap5 import FloatingField


sems = (
    ('semester 1', 'SEMESTER 1'),
    ('semester 2', 'SEMESTER 2')
)

class UserForm(UserCreationForm):
    '''The user creation form.
    It will work together with the student form.
    '''
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
    """Student form for creating students instance"""
    admission_date = forms.DateField(widget=DateInput)
    dob = forms.DateField(widget=DateInput)
    class Meta:
        model = Student
        widgets = {
          'address': forms.Textarea(attrs={'rows':2})
        }
        fields =  ['faculty', 'courses','mobile_number', 'address', 'gender','dob', 'admission_date', 'image']


class ComplaintForm(forms.ModelForm):
    """Complaint form
    Students can use to send complaints.
    """
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
    """Form to update student."""
    class Meta:
        model = Student
        fields = ['image', 'faculty', 'courses', 'address', 'mobile_number']


class PaymentForm(forms.ModelForm):
    """The payment form to create payment instances"""
    date_paid = forms.DateField(widget=DateInput)
    class Meta:
        model = Payment
        fields = ['student','academic_year', 'semester', 'amount', 'payment_method', 'date_paid']

class PaymentUpdateForm(forms.ModelForm):
    """Form to update payment"""
    class Meta:
        model = Payment
        fields = ['student','academic_year', 'semester', 'amount', 'payment_method']


class DeactivateStudent(forms.Form):
    """Deactivate user form"""
    deactivate = forms.BooleanField()
    

class ComplaintFixedForm(forms.Form):
    """Updating complaint status when resolved"""
    STATUS  =( 
        ('', '----'),
        ('P', 'Pending'),
        ('R', 'Resolved'),
        ('C', 'Closed')
    )
    status = forms.ChoiceField(choices=STATUS)

class AdminForm(forms.ModelForm):
    pass


class CustomSubmit(BaseInput):
    input_type = "submit"
    field_classes = "btn btn-outline-primary"


# search feature for payment
class PaymentFilterForm(forms.Form):
    """Form for filtering and searching payment records"""
    payment_id = forms.CharField(required=False)
    start_date = forms.DateField(widget=DateInput)
    end_date = forms.DateField(widget=DateInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                FloatingField("payment_id", wrapper_class='col-md-3'),
                FloatingField("start_date", wrapper_class='col-md-3'),
                FloatingField("end_date", wrapper_class='col-md-3'),
                Div(
                    CustomSubmit(
                        'submit', 
                        'filter result',  
                        css_class="btn-lg col-12"
                    ), 
                    css_class='col-md-3',        
                )  
            ),
        )

        
        
class StudentSearchForm(forms.Form):
    """Form to filter and search students records"""
    query = forms.CharField(
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['query'].label = ''
        self.fields['query'].widget.attrs.update({
            'class': 'form-control form-control-lg mb-0',
            'placeholder': 'Search by student name, student id',
    })
        

class ComplaintFilterForm(forms.Form):
    """Form to filter complaint records."""
    STATUS  =( 
        ('', '----'),
        ('P', 'Pending'),
        ('R', 'Resolved'),
        ('C', 'Closed')
    )
    reference_id = forms.CharField(required=False)
    status = forms.ChoiceField(choices=STATUS, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            Row(
                FloatingField("reference_id", wrapper_class='col-md-4'),
                FloatingField("status", wrapper_class='col-md-4'),
                Div(
                    Submit('submit', 'filter',  css_class="col-12 col-md-8 btn-lg btn-primary"), 
                    css_class='col-md-4',        
                )    
            ),
        )
        

    
