from django.urls import path
from .views import CreateOrderViewRemote, CaptureOrderView
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    # path('stripe-webhook/', stripe_webhook_view, name='stripe-webhook'),
    path("create-checkout-session/<pk>/",CreateOrderViewRemote.as_view(),name='chechout-session'),
    path('paypal/capture/order', CaptureOrderView.as_view(), name='captureorder'),
]
