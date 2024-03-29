from rest_framework import serializers
from .models import Blog, Registration, Payment, Query
from .razorpay import Razorpay

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ('id', 'title', 'content', 'image_path', 'created_at', 'description', 'category')
        

class QuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Query
        fields = ('id', 'name', 'email', 'phone_number', 'message')


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = ('id', 'name', 'phone_number', 'whatsapp_number', 'email', 'gender', 
                  'course', 'batch', 'status', 'amount')
        
    def add_registeration(self, *args, **kwargs):
      print("validated data  ;", self.validated_data)
      order_data = {'amount': int(self.validated_data.get('amount'))}
      registration = super().create(self.validated_data)
      
      payment_details = Razorpay().create_payment_link(self.validated_data, registration.id)
      payment_data = {
        # "order_id" : order['id'],
        "amount" : int(self.validated_data.get('amount')),
        "description" : 'Payment for IYT',
        "status": 'P',
        "payment_link": payment_details.get("short_url"),
        "plid": payment_details.get("id"),
        "additional_data": {'create': payment_details}
      }
      payment_serializer = PaymentSerializer(data=payment_data)
      payment_serializer.is_valid(raise_exception=True)
      payment = payment_serializer.save()
    #   self.validated_data['payment_id'] = payment.id
      registration.payment_id = payment.id
      registration.save()
    #   registration = super().create(self.validated_data)
      return {'registration_id': registration.id}
      
      
      

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'