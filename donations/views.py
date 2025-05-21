import stripe
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Donation
from .serializers import DonationSerializer
from blogs.permissions import IsSuperUserOrReadOnly
from rest_framework import generics

stripe.api_key = settings.STRIPE_SECRET_KEY


# class CreateCheckoutSession(APIView):
#     def post(self, request):
#         serializer = DonationSerializer(data=request.data)
#         if serializer.is_valid():
#             # Save donation record
#             donation = Donation.objects.create(
#                 amount=serializer.validated_data['amount'],
#                 email=serializer.validated_data['email'],
#                 full_name = serializer.validated_data['full_name'],
#                 location = serializer.validated_data['location'],  
#             )

#             # Create Stripe Checkout Session
#             try:
#                 checkout_session = stripe.checkout.Session.create(
#                     payment_method_types=['card'],
#                     line_items=[
#                         {
#                             'price_data': {
#                                 'currency': 'usd',
#                                 'unit_amount': int(donation.amount * 100),  # Convert to cents
#                                 'product_data': {
#                                     'name': "Donation",
#                                 },
#                             },
#                             'quantity': 1,
#                         },
#                     ],
#                     mode='payment',  # Only one-off payments
#                     customer_email=donation.email,
#                     success_url='http://localhost:8000/success?session_id={CHECKOUT_SESSION_ID}',
#                     cancel_url='http://localhost:8000/',  # Redirect to homepage on cancel
#                 )
#                 donation.stripe_session_id = checkout_session.id
#                 donation.save()
#                 return Response({'sessionId': checkout_session.id}, status=status.HTTP_200_OK)
#             except Exception as e:
#                 return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateCheckoutSession(APIView):
    def post(self, request):
        serializer = DonationSerializer(data=request.data)
        
        if serializer.is_valid():
            donation = Donation.objects.create(
                email=serializer.validated_data['email'],
                full_name=serializer.validated_data.get('full_name'),
                location=serializer.validated_data.get('location'),
                amount=serializer.validated_data['amount'],
            )
            print(donation)

            try:
                session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=[{
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {'name': 'Donation'},
                            'unit_amount': int(donation.amount * 100),  # cents
                        },
                        'quantity': 1,
                    }],
                    
                    mode='payment',
                    customer_email=donation.email,
                    success_url='http://localhost:8000/success?session_id={CHECKOUT_SESSION_ID}',
                    cancel_url='http://localhost:8000/',
                )
                print("Session:",session)

                donation.stripe_session_id = session.id
                donation.stripe_session_url = session.url
                donation.save()
                return Response({'sessionId': session.id, 'sessionUrl':session.url}, status=200)

            except Exception as e:
                return Response({'error': str(e)}, status=400)

        return Response(serializer.errors, status=400)

class PaymentSuccessView(APIView):
    def get(self, request):
        session_id = request.GET.get('session_id')
        if not session_id:
            return Response({'error': 'Missing session ID'}, status=400)

        donation = Donation.objects.filter(stripe_session_id=session_id).first()
        if donation and donation.payment_status != 'completed':
            donation.payment_status = 'completed'
            donation.save()
            return Response({'message': 'Payment completed.'})
        return Response({'error': 'Invalid or already completed.'}, status=400)

class StripeWebhookView(APIView):
    def post(self, request):
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
        endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

        try:
            event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
        except ValueError:
            return Response({'error': 'Invalid payload'}, status=400)
        except stripe.error.SignatureVerificationError:
            return Response({'error': 'Invalid signature'}, status=400)

        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            donation = Donation.objects.filter(stripe_session_id=session.get('id')).first()
            if donation:
                donation.payment_status = 'completed'
                donation.save()

        return Response({'status': 'success'}, status=200)


class AllDonationList(generics.ListAPIView):
    queryset = Donation.objects.all().order_by('-created_at')
    serializer_class = DonationSerializer
    permission_classes = [IsSuperUserOrReadOnly]
    