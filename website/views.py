from rest_framework import viewsets
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Blog, Registration, Query, Batches
from .serializers import BlogSerializer, RegistrationSerializer, QuerySerializer
import traceback
from .utils import trigger_error_email

class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

# 100: {
#     text: "100 Hrs Teacher Training",
#     fee: "499",
#     slots: [{value:"April", label:"April 2023 (1st - 12th)"},
#             {value:"May", label:"May 2023 (1st - 12th)"},
#             {value:"June", label:"June 2023 (1st - 12th)"},
#             {value:"July", label:"July 2023 (1st - 12th)"}]
#   },
class BatchViewSet(viewsets.ModelViewSet):
    queryset = Batches.objects.all()
    
    @action(detail=False, methods=['get'])
    def get_batches(self, request, *args, **kwargs):
        batches = self.queryset.filter(is_active=True).values("id","month","year","start_date","end_date","fee","course__title","course__hrs")
        data = {}
        for batch in batches:
            batch_name = batch["month"]+" "+ batch["year"]+" ("+batch["start_date"]+" - "+batch["end_date"]+")"
            if batch["course__hrs"] in data:
                course = data[batch["course__hrs"]]
                course["slots"].append({"value":batch["id"], "label": batch_name})
            else:
                data[batch["course__hrs"]] = {
                    "text": batch["course__title"],
                    "fee": batch["fee"],
                    "slots": [{"value":batch["id"], "label": batch_name}]
                }
                # data[batch["course__hrs"]] = [batch_name]
        return Response({"batches":data,"status":"success"}, status=status.HTTP_200_OK)
        
    
class QueryViewSet(viewsets.ModelViewSet):
    queryset = Query.objects.all()
    serializer_class = QuerySerializer
    
    @action(detail=False, methods=['post'])
    def add(self, request, *args, **kwargs):
        # request.data.remove('amount')
        # import ipdb;ipdb.set_trace()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                response = serializer.save()
                return Response({"status":"success"}, status=status.HTTP_201_CREATED)
            except Exception as e:
                error = str(e)
                return Response({"error":error,"status":"failed"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            print(traceback.format_exc)
            trigger_error_email(str(serializer.__dict__))
            return Response({"errors":serializer.errors, "status":"failed"}, status=status.HTTP_400_BAD_REQUEST)

class RegistrationViewSet(viewsets.ModelViewSet):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
    
    @action(detail=False, methods=['post'])
    def checkout(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            response = serializer.add_registeration(request.data)
            response['status'] = "success"
            return Response({"data":response}, status=status.HTTP_201_CREATED)
        else:
            print(traceback.format_exc())
            trigger_error_email(str(serializer.__dict__))
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
            print(res)
            trigger_error_email(str(res))
            return Response({"status":"failed"}, status=status.HTTP_400_BAD_REQUEST)
        
