from rest_framework import viewsets
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Blog, Registration
from .serializers import BlogSerializer, RegistrationSerializer
import traceback


class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

class RegistrationViewSet(viewsets.ModelViewSet):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
    
    @action(detail=False, methods=['post'])
    def checkout(self, request, *args, **kwargs):
        #import ipdb;ipdb.set_trace()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            response = serializer.add_registeration(request.data)
            response['status'] = ["success"] 
            return Response({"data":response}, status=status.HTTP_201_CREATED)
        else:
            print(traceback.format_exc)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def success(self, request, *args, **kwargs):
        # request_data   => {'razorpay_payment_id': 'pay_Lg6B920QvU9mBj', 'razorpay_order_id': 'order_Lg6ArZMgl3agZf', 'razorpay_signature': '86028154e3f005ed6180359730fed27071291a21c6384acbde3a871ab0f84ad7'}
        registration_id = request.data.get('registeration_id')
        payment_id = request.data.get('razorpay_payment_id')
        registration = Registration.objects.get(id=registration_id)
        res = registration.order_successful(payment_id)
        if res['status'] == 'Success':
            return Response({"status":"success"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status":"failed"}, status=status.HTTP_201_CREATED)
        
