from django.urls import path
from .views import index, addUser, student, update_student, payment, update_payment, delete_payment

urlpatterns = [
    path('', index, name="index"),
    path('adduser/', addUser, name="adduser"),
    path('students/all/', student, name="students"),
    path('students/update/<str:username>', update_student, name="update_student"),
    path('payment/', payment, name="make_payment"),
    path('payment/update/<int:pk>', update_payment, name="update_payment"),
    path('payment/delete/', delete_payment, name="delete_payment"),
]