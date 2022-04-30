from django.urls import path
from .views import index, addUser

urlpatterns = [
    path('', index, name="index"),
    path('adduser/', addUser, name="index"),
]