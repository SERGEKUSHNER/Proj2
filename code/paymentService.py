
import random

class PaymentService:

    @classmethod
    def CheapPaymentGateway(self):
        print("Cheap Payment Gatway is used with success")
        return 1

    @classmethod
    def ExpensivePaymentGateway(self):
        print("ExpensivePaymentGateway is used with success")
        return 2

    @classmethod
    def PremiumPaymentGateway(self):
        print("Premium Payment Gateway is used with success")
        return 3

    @classmethod
    def PaymentAvailability(self):
        randNumber = random.randint(1, 101)
        print(randNumber)
        if randNumber > 50:
            print("Expensive Payment Service is available")
            return True
        else:
            print("Expensive Payment Service is not available")
            return False


