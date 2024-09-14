from django.urls import path
from .views import (
    payment_proof
)


urlpatterns = [
    path('student/payment/proof', payment_proof, name="payment_proof"),
]