from .models import CustomUser
from DjangoBlog.utils import sendEmail
from DjangoBlog.permission import IsOwnerOrReadOnly
from .serializers import UserRegisterSerializer,LoginSerializer,UserProfileSerialzer

import jwt

from django.urls import reverse
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site

from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

JWT_PAYLOAD_HANDLER=api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER=api_settings.JWT_ENCODE_HANDLER


class UserRegisterAPIView(generics.CreateAPIView):
    queryset=CustomUser.objects.all()
    serializer_class=UserRegisterSerializer
    
    def post(self, request,*args,**kwargs):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data=serializer.data
        email=user_data['email']
        user=CustomUser.objects.get(email=email)
        
        current_site=get_current_site(request).domain
        reverse_link=reverse('verify-email')
        token=RefreshToken.for_user(user).access_token
        absurl="http://"+current_site+reverse_link+"?token="+str(token)
        
        body="Almost done,<br>"+user_data['name']+" to secure your account, we just need to verify your email address: "+email+"."+"<br>This will let you receive notification and password reset."+"<br> Click the following link or paste it into your browser: <br> "+absurl
        data={
            'subject':"Email verification for new user",
            'message':body,
            'from_email':email,
        }
        sendEmail(data)
        response={
            'success':True,
            'status':status.HTTP_200_OK,
            'message':"A verification link has been send to your registered email address."
        }
        return Response(response)
    
class EmailVerificationAPIView(generics.GenericAPIView):
    def get(self,request):
        token=request.GET.get('token')
        try:
            payload=jwt.decode(token,settings.SECRET_KEY,algorithms=['HS256',])
            user=CustomUser.objects.get(id=payload['user_id'])
            user.is_active=True
            user.is_staff=True
            user.save()
            return Response({"Success Message: ":"Your has been verified ans successfully verified."})
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error':"Activation link expires."})
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error':"invalid token."})
            
class LoginAPIView(generics.GenericAPIView):
    queryset=CustomUser.objects.all()
    serializer_class=LoginSerializer
    
    def post(self,request,*args,**kwargs):
        serializer=self.serializer_class(data=request.data,context={'request':request})
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data['user']
        try:
            payload=JWT_PAYLOAD_HANDLER(user)
            jwt_token=JWT_ENCODE_HANDLER(payload)
            login(request,user)
            response={
            'user':user.name,
            'email':user.email,
            'token':jwt_token,
            'message':'you are successfully logged in.'
        }
        except request.user.is_anonymous:
            print("Not a valid user")
            response={
                'msg':"the user is anonymus"
            }    
        return Response(response)

class UserDetailUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset=CustomUser.objects.all()
    serializer_class=UserProfileSerialzer
    lookup_field='pk'
    permission_classes=[IsAuthenticated]
    
    # def get(self, request,pk):
    #     queryset=CustomUser.objects.get(pk=pk)
    #     serializer=self.serializer_class(queryset,context={'request':request})
    #     return Response(serializer.data)
    