from django.urls import path
from .views import (
    staff_profile, 
    current_user_dashboard,
    user_settings
)


urlpatterns = [
    path('staff/<str:username>', staff_profile, name="staff_profile"),
    path('users/settings', user_settings, name='user_settings'),
    path('', current_user_dashboard, name="currentdashboard"),
]