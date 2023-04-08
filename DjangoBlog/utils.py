from django.core.mail import send_mail
from django.conf import settings

def sendEmail(data):
    send_mail(subject=data['subject'], 
              message=data['message'], 
              from_email=settings.EMAIL_HOST_USER, 
              recipient_list=[data['from_email']]
              )