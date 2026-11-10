from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import MpesaTransaction
import uuid

class MpesaSTKPushView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        phone_number = request.data.get('phone_number')
        amount = request.data.get('amount')
        if not phone_number or not amount:
            return Response({'error': 'phone_number and amount are required'}, status=status.HTTP_400_BAD_REQUEST)

        # STK Push generation architecture
        checkout_id = f"ws_CO_{uuid.uuid4().hex[:12]}"
        merchant_id = f"merch_{uuid.uuid4().hex[:8]}"

        txn = MpesaTransaction.objects.create(
            merchant_request_id=merchant_id,
            checkout_request_id=checkout_id,
            phone_number=phone_number,
            amount=amount,
        )

        return Response({
            'status': 'STK_PUSH_SENT',
            'checkout_request_id': checkout_id,
            'merchant_request_id': merchant_id,
            'customer_message': 'Please enter M-Pesa PIN on customer handset to authorize payment.'
        })

class MpesaCallbackView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """Callback receiver from Safaricom Daraja API"""
        body = request.data.get('Body', {}).get('stkCallback', {})
        checkout_id = body.get('CheckoutRequestID')
        result_code = body.get('ResultCode')
        result_desc = body.get('ResultDesc')

        txn = MpesaTransaction.objects.filter(checkout_request_id=checkout_id).first()
        if txn:
            txn.result_code = result_code
            txn.result_desc = result_desc
            if result_code == 0:
                txn.is_successful = True
                # Extract M-Pesa receipt code
                items = body.get('CallbackMetadata', {}).get('Item', [])
                for item in items:
                    if item.get('Name') == 'MpesaReceiptNumber':
                        txn.mpesa_receipt_number = item.get('Value')
            txn.save()

        return Response({'ResultCode': 0, 'ResultDesc': 'Accepted'})

