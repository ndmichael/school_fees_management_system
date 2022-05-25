from django.urls import path
from .views import (
    index, addStudent, student, update_student, 
    payment, update_payment, delete_payment, admin_dashboard,
    payment_report, payment_detail
)

urlpatterns = [
    path('', index, name="index"),
    path('admin-dashboard/', admin_dashboard, name="admin_dashboard"),
    path('adduser/', addStudent, name="addstudent"),
    path('students/all/', student, name="students"),
    path('students/update/<str:username>/', update_student, name="update_student"),
    path('payment/', payment, name="make_payment"),
    path('payment/update/<int:pk>/', update_payment, name="update_payment"),
    path('payment/report/',payment_report, name="payment_report"),
    path('payment/details/<int:id>', payment_detail, name="payment_detail"),
    path('payment/delete/', delete_payment, name="delete_payment"),
]