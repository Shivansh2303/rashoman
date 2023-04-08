from django.db import models
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save

UserModel=get_user_model()

class Payment(models.Model):
    user=models.ForeignKey(UserModel, on_delete=models.CASCADE)
    payment_success=models.BooleanField(default=False)
    checkout_id=models.CharField(max_length=500)
    
@receiver(post_save, sender=UserModel)
def user_payment(sender,instance,created, **kwargs):
    if created:
        UserPayment.objects.create(user=instance)
    
