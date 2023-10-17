import razorpay
import time

SUCCESS_STATUS = ['authorized']

class Razorpay():
    def __init__(self) -> None:
        self.key = 'rzp_test_wKneKRVvtIi1DS'
        self.secret = 'xnEFDC5fNL78oaMaGLijdgDg'
        self.razorpay_client = razorpay.Client(auth=(self.key, self.secret))

    
    def create_order(self, data):
        amount = data.get("amount")  # Replace with the actual amount
        currency = 'INR'  # Replace with the actual currency code
        order = self.razorpay_client.order.create({'amount': amount, 'currency': currency})
        return order
    
    def create_payment_link(self, data, order_id):
        time_now = time.time()
        expiry = int(time_now + 259200)
        print("expiry ",expiry)
        res = self.razorpay_client.payment_link.create({
                "upi_link": False,
                "amount": int(data.get("amount")),
                "currency": "INR",
                "accept_partial": False,
                "first_min_partial_amount": 100,
                "description": "For IYT Registration",
                "customer": {
                    "name": data.get("name"),
                    "email": data.get("email"),
                    "contact": data.get("phone_number")
                },
                "notify": {
                    "sms": True,
                    "email": True,
                    "whatsapp": True
                },
                "reminder_enable": True,
                "expire_by": expiry,
                "notes": {
                    "course": data.get("course"),
                    "order_id": order_id
                }
                })
        return res
    
    def validate_pyment(self, payment_id, amount):
        res = self.razorpay_client.payment.fetch(payment_id)
        if res['status'] in SUCCESS_STATUS:
            return res
        else:
            return {}