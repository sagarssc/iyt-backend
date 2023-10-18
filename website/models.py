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


class Course(TimeStamp):
    title = models.CharField(max_length=255)
    hrs = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)
    
    def __str__(self) -> str:
        return str(self.id)+" :- "+self.title
    
class Batches(TimeStamp):
    month = models.CharField(max_length=255)
    year = models.CharField(max_length=10)
    start_date = models.CharField(max_length=15)
    end_date = models.CharField(max_length=15)
    fee = models.CharField(max_length=6, null=True)
    is_completed = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    

class Payment(TimeStamp):
    STATUS_CHOICES = [
        ('P', 'Pending'),
        ('C', 'Completed'),
        ('F', 'Failed'),
        ('R', 'Refunded'),
        ('E', 'Expired'),
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
    
    def __str__(self) -> str:
        return str(self.id) +":-   "+str(self.payment_link)


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
    cancellation_reason = models.CharField(max_length=255, null=True)
    additional_data = models.JSONField(default=dict, null=True)
    registration_no = models.CharField(max_length=16, null=True)
    
    def order_successful(self):
        try:
            if self.registration_no:
                raise Exception("Registration no already generated.")
            self.status = 'S'
            self.registration_no = self.generate_registration_no()
            self.save()
            trigger_email(self.registration_no, self.name, self.email, self.phone_number)
            return {"status": "Success"}
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