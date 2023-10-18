from django.core.management.base import BaseCommand
from datetime import datetime
from website.models import Payment, Registration
from website.razorpay import Razorpay
import time
class Command(BaseCommand):
    help = 'Script for updating Completed Payments'

    def handle(self, *args, **options):
        # Your logic here
        registrations = Registration.objects.filter(status="P")
        for registration in registrations:
          payment = registration.payment
          razorpay = Razorpay()
          if payment and payment.plid:
            now = time.time()
            res = razorpay.get_pyayment_status(payment.plid)
            if res["status"] == "paid":
              additional_data = payment.additional_data
              additional_data.update({"payment_response": res})
              payment.additional_data = additional_data
              payment.status = "C"
              payment.save()
              registration.order_successful()
            if res and res["expire_by"] < now:
              additional_data = payment.additional_data
              additional_data.update({"payment_response": res})
              payment.additional_data = additional_data
              payment.status = "E"
              payment.save()
              registration.status = "C"
              registration.cancellation_reason = "Payment Link Expired"
              registration.save()
        return
