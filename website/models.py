from django.db import models
from django.utils import timezone
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .razorpay import Razorpay
from .utils import trigger_email, trigger_error_email
import traceback
from datetime import date
from django.db.models import Max
# from django_mysql.models import JSONField

class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Blog(TimeStamp):
    title = models.CharField(max_length=200)
    content = models.JSONField()
    category = models.CharField(max_length=50)
    image_path = models.TextField()
    description = models.CharField(max_length=500)

class Payment(TimeStamp):
    STATUS_CHOICES = [
        ('P', 'Pending'),
        ('C', 'Completed'),
        ('F', 'Failed'),
        ('R', 'Refunded'),
    ]
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    order_id = models.CharField(max_length=255, null=True)
    txn_id = models.CharField(max_length=255, null=True)
    payment_link = models.CharField(max_length=255, null=True)
    plid = models.CharField(max_length=255, null=True)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    additional_data = models.JSONField(default=dict)
    # client.payment_link.fetch(paymentLinkId)


class Registration(TimeStamp):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    STATUS_CHOICES = [
        ('P', 'Pending'),
        ('S', 'Successful'),
        ('C', 'Cancelled'),
    ]
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    whatsapp_number = models.CharField(max_length=15)
    email = models.EmailField()
    course = models.CharField(max_length=255)
    batch = models.CharField(max_length=15)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    cancelation_reason = models.CharField(max_length=255, null=True)
    additional_data = models.JSONField(default=dict)
    registration_no = models.CharField(max_length=16)
    
    def order_successful(self, payment_id):
        try:
            razorpay = Razorpay()
            res = razorpay.validate_pyment(payment_id, self.payment)
            if res:
                self.status = 'S'
                self.registration_number = self.generate_registration_no()
                self.save()
                self.payment.status = 'C'
                self.payment.txn_id = payment_id
                self.payment.save()
                trigger_email(self.registration_number, self.name, self.email, self.phone_number)
                return {"status": "Success"}
            else:
                return {"status": "Failed","reason": "payment validation failed"}
        except Exception as e:
            print(traceback.format_exc())
            trigger_error_email(str(traceback.format_exc()))
            return {"status": "Failed","reason": "payment validation failed"}  
    
    def generate_registration_no(self):
        try:
            current_date = date.today().strftime('%y%m%d')

            # Get the latest registration number with the current date
            latest_registration = Registration.objects.filter(
                registration_no__startswith=f'IYT-{current_date}-'
            ).aggregate(Max('registration_no'))['registration_no__max']

            if latest_registration:
                # Extract the last five digits, increment by 1, and format as 5-digit string
                latest_number = int(latest_registration[-5:]) + 1
            else:
                # If there are no existing registrations for the current date, start from 1
                latest_number = 1

            # Format the registration number
            registration_number = f'IYT-{current_date}-{latest_number:05d}'

            return registration_number
        except Exception as e:
            print(traceback.format_exc())
            trigger_error_email(str(traceback.format_exc()))
            return {"status": "Failed","reason": "payment validation failed"}    
        

class Query(TimeStamp):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    message = models.TextField()