from rest_framework.views import APIView

from .tasks import process_mo
from .models import SMSDR, MTSent


class SMSMO(APIView):
    def post(self, request, format=None):
        from_number = request.data.get('From')
        # Receiver's phone number - Plivo number
        to_number = request.data.get('To')
        # The text which was received
        content = request.data.get('Text')

        # Print the message
        print('Message received - From: %s, To: %s, Text: %s' % (from_number, to_number, content))

        # Process MO
        process_mo.delay(from_number, to_number, content)

        return "Message received", 200


class SMSDR(APIView):
    def post(self, request, format=None):
        # Sender's phone number
        from_number = request.data.get('From')
        # Receiver's phone number - Plivo number
        to_number = request.data.get('To')
        # Status of the message
        status = request.data.get('Status')
        # Message UUID
        uuid = request.data.get('MessageUUID')

        # Fetch the MT Sent entry to tag the DR (delivery report)
        mt_sent = MTSent.objects.get(aggregator_id=uuid)

        SMSDR.objects.create(
            from_phone_number=from_number,
            to_phone_number=to_number,
            mt_sent=mt_sent,
            status=status,
        )

        # Prints the status of the message
        print("From: %s, To: %s, Status: %s, MessageUUID: %s" % (from_number, to_number, status, uuid))
        return "Delivery status reported"
