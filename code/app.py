from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required, current_identity
from datetime import datetime
from paymentService import PaymentService

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True  # To allow flask propagating exception even if debug is set to false on app

api = Api(app)


items = []


class Item(Resource):

    def check_positive(value):
        ivalue = int(value)
        if ivalue < 0:
            raise argparse.ArgumentTypeError("%s is an invalid positive int value" % value)
        return ivalue

    def checkDigits(value):
        ivalue = len(value)
        if ivalue == 3:
            ivalue = int(value)
            if ivalue >= 0:
                return value
            else:
                raise argparse.ArgumentTypeError("%s should be a positive number from 3 digits" % value)
        else:
            raise argparse.ArgumentTypeError("%s should be a positive number from 3 digits" % value)

    def valid_date(s):
        try:
            present = datetime.now()

            print(present)
            obj = datetime.strptime(s, "%Y-%m-%d")
            print(obj)
            if present.year <= obj.year and present.month <= obj.month and present.day <= obj.day:
                obj = obj.replace(hour=23, minute=59, second=59, microsecond=0).isoformat()
                return obj
            else:
                msg = "Date should not be in the past: '{0}'.".format(s)
                raise argparse.ArgumentTypeError(msg)
        except ValueError:
            msg = "Not a valid date: '{0}'.".format(s)
            raise argparse.ArgumentTypeError(msg)

    parser = reqparse.RequestParser()
    parser.add_argument('creditCardNumber',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('cardHolder',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('expirationDate',
                        type=valid_date,
                        help="Date cannot be in the past and format date is: YYYY-MM-DD"
                        )
    parser.add_argument('securityCode',
                        type=checkDigits,
                        help="security Code should contain 3 positive digits!"
                        )
    parser.add_argument('Amount',
                        type=check_positive,
                        required=True,
                        help="Amount should be positive"
                        )

    def post(self):
        data = Item.parser.parse_args()
        if next(filter(lambda x: x['creditCardNumber'] == data['creditCardNumber'], items), None) is not None:
            return {'message': "This creditCardNumber already exists."}

        item = {
            'creditCardNumber': data['creditCardNumber'],
            'cardHolder': data['cardHolder'],
            'expirationDate': data['expirationDate'],
            'securityCode': data['securityCode'],
            'Amount': data['Amount'],
        }
        items.append(item)
        if data['Amount'] < 21:
            PaymentService.CheapPaymentGateway()
        if data['Amount'] in range(21, 501):
            if PaymentService.PaymentAvailability():
                PaymentService.ExpensivePaymentGateway()
            else:
                PaymentService.CheapPaymentGateway()
        if data['Amount'] > 500:
            for x in range(3):
                if PaymentService.PaymentAvailability():
                    PaymentService.PremiumPaymentGateway()
                    break

        return item

    def get(self):
         return {'items': items}


api.add_resource(Item, '/item/')


if __name__ == '__main__':
    app.run(debug=True)  # important to mention debug=True
