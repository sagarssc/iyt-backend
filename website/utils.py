from .models import Payment, Registration


def validate_payment(payment_id):
    payment = Payment.objects.get(id=payment_id)
    
    