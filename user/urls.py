from django.urls import path
from .views import student_profile

urlpatterns = [
    path('student/<str:username>/', student_profile, name="stud_profile"),
]