from django.db import models
from django.contrib.auth import get_user_model
from article.models import Article

UserModel=get_user_model()

class PaymentHistory(models.Model):
    owner=models.ForeignKey(UserModel, on_delete=models.CASCADE, blank=True, null=True)
    blog=models.ForeignKey(Article, on_delete=models.SET_NULL, blank=True, null=True)
    date=models.DateTimeField(auto_now_add=True)
    payment_status=models.BooleanField()


    def __str__(self):
        return self.blog.title