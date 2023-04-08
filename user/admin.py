from django.contrib import admin
# from django.contrib.auth import get_user_model
# user=get_user_model()
from .models import CustomUser
admin.site.register(CustomUser)