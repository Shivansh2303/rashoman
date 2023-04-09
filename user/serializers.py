from .models import CustomUser

from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login

from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from rest_framework.response import Response

class UserRegisterSerializer(serializers.ModelSerializer):
    profile_image=serializers.ImageField(allow_null=True,allow_empty_file=True)
    is_active=serializers.BooleanField(read_only=True)
    is_staff=serializers.BooleanField(read_only=True)
    password=serializers.CharField(required=True,write_only=True)
    
    class Meta:
        model=CustomUser
        fields=['id','name','email','profile_image','date_joined','updated_at','is_active','is_staff','password']
        
    def create(self, validated_data):
        password=validated_data.pop('password',None)
        instance=self.Meta.model(**validated_data)
        email=validated_data['email']
        user=CustomUser.objects.filter(email=email)
        user.is_staff=True
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    

class LoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(required=True)
    password=serializers.CharField(required=True)
    
    class Meta:
        model=CustomUser
        fields=('email','password')
    
    def validate(self, attrs):
        email=attrs['email']
        password=attrs['password']
        
        if email and password:
            user=authenticate(request=self.context.get('request'),email=email,password=password)
            if not user:
                msg=("Unable to login with provided credentials")
                raise serializers.ValidationError(msg,code='authentication')
        else:
            msg=("Must include 'email' and 'password'.")
            raise serializers.ValidationError(msg,code='authentication')
        attrs['user']=user
        return attrs

class UserProfileSerialzer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields=['id','name','email','date_joined','profile_image']