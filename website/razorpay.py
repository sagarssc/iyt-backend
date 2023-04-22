import razorpay

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
    
    def validate_pyment(self, payment_id, amount):
        res = self.razorpay_client.payment.fetch(payment_id)
        if res['status'] in SUCCESS_STATUS:
            return res
        else:
            return {}