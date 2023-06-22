from django.urls import path
from .views import stud_profile, student_profile, staff_profile


urlpatterns = [
    path('student/<str:username>/profile', stud_profile, name="stud_profile"),
    path('staff/<str:username>/profile', staff_profile, name="staff_profile"),
    path('student/<str:username>/', student_profile, name="student_profile"),
]