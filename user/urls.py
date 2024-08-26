from django.urls import path
from .views import (
    student_profile, 
    staff_profile, 
    current_user_profile,
    user_settings
)


urlpatterns = [
    path('staff/<str:username>', staff_profile, name="staff_profile"),
    path('student/<str:username>', student_profile, name="student_profile"),
    path('users/settings', user_settings, name='user_settings'),
    path('', current_user_profile, name="currentprofile"),
]