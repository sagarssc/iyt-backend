from django.contrib import admin
from .models import Blog
# Register your models here.
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'image_path','content')  # Fields to display in the admin view
    search_fields = ('title', 'category')  # Enable searching by title and category
    list_filter = ('category',)
