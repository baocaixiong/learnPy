# coding: utf8
# stdlib
from json import dumps, loads
from datetime import datetime

# Zato
from zato.server.service import Service

class GetClientDetails(Service):

    class SimpleIO:
        input_required = ('cust_id', 'cust_type')
        output_required = ('first_name', 'last_name',
            'last_payment_date', 'last_payment_amount')

    def should_notify_frauds(self, cust_type):
        config_key = 'myapp:fraud-detection:cust-type'
        return cust_type in self.kvdb.conn.lrange(config_key, 0, -1)

    def handle(self):

        request = dumps(self.request.input)

        # self.logger.info('Request: {}'.format(self.request.payload))
        # self.logger.info('Request type: {}'.format(type(self.request.payload)))

        # # Fetch connection to CRM
        # crm = self.outgoing.plain_http.get('CRM')

        # # Fetch connection to Payments
        # payments = self.outgoing.plain_http.get('Payments')

        # # Grab the customer info ..
        # cust = crm.conn.send(dumps(self.request.payload))
        # cust = loads(cust.text)

        # # .. and last payment's details
        # last_payment = payments.conn.send(dumps(self.request.payload))
        # last_payment = loads(last_payment.text)

        # self.logger.info('Customer details: {}'.format(cust))
        # self.logger.info('Last payment: {}'.format(last_payment))

        cust = {'firstName': 'zhang', 'lastName': 'ming'}
        last_payment = {'DATE': '2013-11-19', 'AMOUNT': '379'}

        response = {}
        response['first_name'] = cust['firstName']
        response['last_name'] = cust['lastName']
        response['last_payment_date'] = last_payment['DATE']
        response['last_payment_amount'] = last_payment['AMOUNT']
        response = dumps(response)

        self.logger.info('Response: {}'.format(response))

        if self.should_notify_frauds(self.request.payload['cust_type']):

            fraud_request = {}
            fraud_request['timestamp'] = datetime.utcnow().isoformat()
            fraud_request['request'] = request
            fraud_request['response'] = response
            fraud_request = dumps(fraud_request)

            self.outgoing.zmq.send(fraud_request, 'Fraud detection')

        else:
            self.logger.info('Skipped fraud detection for CID {}'.format(self.cid))

        # And return response to the caller
        self.response.payload = response

