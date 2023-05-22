from django.urls import path
from .views import stud_profile, student_profile


urlpatterns = [
    path('student/<str:username>/profile', stud_profile, name="stud_profile"),
    path('student/<str:username>/', student_profile, name="student_profile"),
]