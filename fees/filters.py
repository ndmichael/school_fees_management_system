from django_filters import CharFilter, FilterSet
from fees.models import Student, Payment
from django import forms


class StudentFilter(FilterSet):
    """Class to filter the Student Model by course or by ID(username)"""
    # user =  CharFilter(
    #     label='', 
    #     field_name='user',  
    #     lookup_expr='icontains',
    #     widget=forms.TextInput(
    # attrs={
    #         "class":"form-control form-control-lg",
    #         "placeholder": "student id",
    #         "max_length":"100"
    #         }
    #     )
    # )
    class Meta:
        model = Student
        fields = ['courses', 'us']