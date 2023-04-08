from django.urls import path

urlpatterns = [
    path("product-page",PaymentAPIView.as_view(),name='payment-api'),
    path("strip-webhoook",StripWebhook.as_view(),name='strip-webhoook'),
]
