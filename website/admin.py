from django.contrib import admin
from .models import Blog, Registration, Payment
# Register your models here.
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'image_path','content')  # Fields to display in the admin view
    search_fields = ('title', 'category')  # Enable searching by title and category
    list_filter = ('category',)



@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ("name", "phone_number", "email", "course", "batch", "amount", "payment", "status", "registration_no")
    
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("amount", "description", "order_id", "txn_id", "payment_link", "plid", "date", "status")