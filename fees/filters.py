from django_filters import CharFilter, FilterSet
from fees.models import Complaint
from django import forms
from crispy_forms.layout import Layout, Submit, Row, Fieldset, Field
from crispy_forms.helper import FormHelper
from crispy_bootstrap5.bootstrap5 import FloatingField
from .forms import ComplaintFilterForm


class ComplaintFilter(FilterSet):
    """Class to filter the Student Model by course or by ID(username)"""
    
    
    class Meta:
        STATUS  =( ('P', 'Pending'),
            ('R', 'Resolved'),
            ('C', 'Closed')
        )
        model = Complaint
        status = forms.ChoiceField(choices=STATUS)
        fields = ['reference_id', 'status']
        fields ={
           'reference_id': ['icontains'] ,
           'status': [''],
        } 
        # form = ComplaintFilterForm

    @property
    def form(self):
        form = super().form

        layout_components = list(Field(k, wrapper_class='form-control-sm col-md-3') for k in form.fields.keys()) + [
            
        ]
        helper = FormHelper()
        helper.form_method = "GET"
        helper.layout = Layout(
            Row(
                *layout_components,
                Submit('submit', 'filter',  css_class="col-md-3 btn-danger"), 
            ),   
            

        )

        form.helper = helper

        return form

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # Your code
    #     self.helper = FormHelper()
    #     self.helper.layout = Layout(
    #         Row(
    #             Field("reference_id", wrapper_class='col-md-6', css_class="row-fluid"),
    #             FloatingField("status", wrapper_class='col-md-6', css_class="row-fluid"),
    #         ),  
    #         Submit('submit', 'Create Account', css_class="col-12 btn-lg btn-danger fw-bold")             
    #     )

    # def __init__(self, *args, **kwargs):
    #     # super(ComplaintFilter, self).__init__(*args, **kwargs)

    #     super().__init__(*args, **kwargs)
    #     self.helper = FormHelper()
    #     self.helper.layout = Layout(
    #         Row(
    #             FloatingField("reference_id", wrapper_class='col-md-6', css_class="row-fluid"),
    #             # FloatingField("status", wrapper_class='col-md-6', css_class="row-fluid"),
    #         ),  
    #         Submit('submit', 'Create Account', css_class="col-12 btn-lg btn-danger fw-bold")             
    #     )