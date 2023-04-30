from django.db import models
from django.utils import timezone
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .razorpay import Razorpay
# from django_mysql.models import JSONField

class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Blog(TimeStamp):
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=50)
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    description = models.CharField(max_length=500)

    def save(self, *args, **kwargs):
        if self.image:
            # generate a unique filename to avoid overwriting existing files
            filename = f'{self.title}_{timezone.now().strftime("%Y%m%d-%H%M%S")}.jpg'
            # save the image to the default storage location
            saved_path = default_storage.save(f'blog_images/{filename}', ContentFile(self.image.read()))
            # set the image field to the path of the saved file
            self.image = saved_path
        super().save(*args, **kwargs)

class Payment(TimeStamp):
    STATUS_CHOICES = [
        ('P', 'Pending'),
        ('C', 'Completed'),
        ('F', 'Failed'),
        ('R', 'Refunded'),
    ]
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    order_id = models.CharField(max_length=255)
    txn_id = models.CharField(max_length=255, null=True)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    additional_data = models.JSONField(default=dict)

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
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    cancelation_reason = models.CharField(max_length=255, null=True)
    additional_data = models.JSONField(default={})
    
    def order_successful(self, payment_id):
        razorpay = Razorpay()
        res = razorpay.validate_pyment(payment_id, self.payment)
        if res:
            self.status = 'S'
            self.save()
            self.payment.status = 'C'
            self.payment.txn_id = payment_id
            self.payment.save()
            return {"status": "Success"}
        else:
            return {"status": "Failed","reason": "payment validation failed"}
        
        

class Query(TimeStamp):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    message = models.TextField()