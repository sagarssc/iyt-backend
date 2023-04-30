from django.urls import path, include
from rest_framework import routers

from .views import BlogViewSet, RegistrationViewSet, QueryViewSet

urlpatterns = []

router = routers.DefaultRouter()
router.register(r'blogs', BlogViewSet)
router.register(r'register', RegistrationViewSet)
router.register(r'query', QueryViewSet)



urlpatterns += router.urls