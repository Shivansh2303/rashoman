import stripe
from django.shortcuts import render,redirect
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView
from article.models import Article
# from django.conf import settings
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions
from django.contrib.auth import get_user_model
from .tokenization import PaypalToken
from DjangoBlog  import settings
import requests
UserModel=get_user_model()

clientID = settings.clientID
clientSecret = settings.clientSecret
print(clientID," ",clientSecret)

"""        PAYPAL CHECKOUT          """
class CreateOrderViewRemote(APIView):

    def get(self, request,pk=None):
        token = PaypalToken(clientID, clientSecret)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer '+token,
        }
        print(token)
        article=Article.objects.get(id=pk)
        user=UserModel.objects.get(id=1)
        print(user)
        json_data = {
             "intent": "CAPTURE",
             "application_context": {
                 "notify_url": "https://pesapedia.co.ke",
                 "return_url": settings.SITE_URL,
                 "cancel_url": settings.SITE_URL,
                 "brand_name": "AWESOME BLOG",
                 "landing_page": "BILLING",
                 "shipping_preference": "NO_SHIPPING",
                 "user_action": "CONTINUE"
             },
             "purchase_units": [
                 {
                     "reference_id": article.id,
                     "description": article.title,

                     "custom_id": "CUST-AfricanFashion",
                     "soft_descriptor": "AfricanFashions",
                     "amount": {
                         "currency_code": "USD",
                         "value": 0.1 ,
                     },
                 }
             ]
         }
        response = requests.post('https://api-m.sandbox.paypal.com/v2/checkout/orders', headers=headers, json=json_data)
        print(response.json())
        # print(response.json.text)
        order_id = response.json()['id']
        linkForPayment = response.json()['links'][1]['href']
        print(linkForPayment)
        return Response(linkForPayment)

class CaptureOrderView(APIView):
    #capture order aims to check whether the user has authorized payments.
    def get(self, request):
        token = request.data.get('token')#the access token we used above for creating an order, or call the function for generating the token
        token="A21AAI5MuAyveDPPl6wXGpOuDvqbxsUdEupiu15upTN2C7Vc-ajWFugUgii_nSgGfVtqoWHK31OrRnBezDKtanKCGXRrUjQCw"
        captureurl = request.data.get('url')#captureurl = 'https://api.sandbox.paypal.com/v2/checkout/orders/6KF61042TG097104C/capture'#see transaction status
        headers = {"Content-Type": "application/json", "Authorization": "Bearer "+token}
        response = requests.post(captureurl, headers=headers)
        return Response(response.json())

"""              STRIPE CHECKOUT                    """
# class CreateStripeCheckoutSession(APIView):
#     # permission_classes=[permissions.IsAuthenticated]
#     def post(self,request,*args, **kwargs):
#         blog_id=self.kwargs['pk']
#         try:
#             blog=Article.objects.get(id=blog_id)
#             checkout=stripe.checkout.Session.create(
#                 line_items=[
#                     {
#                         'price_data':{
#                             'currency':"usd",
#                             'unit_amount':200,
#                             'product_data':{
#                                 'name':Article.title,
#                             }
#                         },
#                         'quantity':1,
#                     },
#                 ],
#                 mode='payment',
#                 metadata={
#                     'blog_id':blog.id
#                 },
#                 success_url=settings.SITE_URL+'?success=true',
#                 cancel_url=settings.SITE_URL+'?canceled=true'
#             )
#             return redirect(checkout_session.url)
        
#         except Exception as e:
#             return Response({'msg':'something went wrong while creating stripe session','error':str(e)})

# @csrf_exempt
# def stripe_webhook_view(request):
#     payload = request.body
#     sig_header = request.META['HTTP_STRIPE_SIGNATURE']
#     event = None

#     try:
#         event = stripe.Webhook.construct_event(
#         payload, sig_header, settings.STRIPE_SECRET_WEBHOOK
#         )
#     except ValueError as e:
#         # Invalid payload
#         return Response(status=400)
#     except stripe.error.SignatureVerificationError as e:
#         # Invalid signature
#         return Response(status=400)

#     if event['type'] == 'checkout.session.completed':
#         session = event['data']['object']

#         print(session)
#         customer_email=session['customer_details']['email']
#         prod_id=session['metadata']['blog_id']
#         product=Article.objects.get(id=prod_id)
#         #sending confimation mail
#         send_mail(
#             subject="payment sucessful",
#             message=f"thank for your purchase your order is ready",
#             recipient_list=[customer_email],
#             from_email="djangomail@gmail.com"
#         )

#         #creating payment history
#         # user=User.objects.get(email=customer_email) or None

#         PaymentHistory.objects.create(blog=product, payment_status=True)
#     # Passed signature verification
#     return HttpResponse(status=200)