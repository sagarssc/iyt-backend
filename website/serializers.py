from rest_framework import serializers
from .models import Blog, Registration, Payment
from .razorpay import Razorpay

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ('id', 'title', 'content', 'image', 'created_at', 'description', 'category')


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = ('id', 'name', 'phone_number', 'whatsapp_number', 'email', 'gender', 
                  'course', 'batch', 'status', 'amount')
        
    def add_registeration(self, *args, **kwargs):
      print("validated data  ;", self.validated_data)
      order_data = {'amount': int(self.validated_data.get('amount'))}
      order = Razorpay().create_order(order_data)
      payment_data = {
        'order_id' : order['id'],
        'amount' : int(self.validated_data.get('amount')),
        'description' : 'Payment for IYT',
        'status': 'P',
        'additional_data': {'create': order}
      }
      payment_serializer = PaymentSerializer(data=payment_data)
      payment_serializer.is_valid(raise_exception=True)
      payment = payment_serializer.save()
      self.validated_data['payment_id'] = payment.id
      registration = super().create(self.validated_data)
      return {'registration_id': registration.id, 'order_id': order['id']}
      
      
      

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'