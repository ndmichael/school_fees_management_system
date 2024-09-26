from django.urls import path
from .views import (
    payment_proof,
    make_payment,
    payment_complaints,
    student_dashboard
)


urlpatterns = [
    path('student-dashboard/', student_dashboard, name="student_dashboard"),
    path('payment/proof/', payment_proof, name="payment_proof"),
    path('make/payment/', make_payment, name="make_payment"),
    path('payment/complaints/', payment_complaints, name="payment_complaints")
]