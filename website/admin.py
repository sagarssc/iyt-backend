from django.contrib import admin
from .models import Blog, Registration, Payment, Course, Batches
# Register your models here.
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'image_path','content')  # Fields to display in the admin view
    search_fields = ('title', 'category')  # Enable searching by title and category
    list_filter = ('category',)



@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ("created_at","updated_at","name", "phone_number", "email", "course", "batch", "amount", "payment", "status", "registration_no")
    
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("created_at","updated_at","amount", "description", "order_id", "txn_id", "payment_link", "plid", "date", "status")
    
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "hrs", "is_active")
    
@admin.register(Batches)
class BatchesAdmin(admin.ModelAdmin):
    list_display = ("month", "year", "start_date", "end_date", "is_completed", "is_active", "course")