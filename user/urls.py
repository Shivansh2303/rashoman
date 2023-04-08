from django.conf.urls.static import static
from django.urls import path,include
from django.conf import settings
from .views import *
urlpatterns = [
    path('user-register/',UserRegisterAPIView.as_view(),name='register'),
    path('user-login/',LoginAPIView.as_view(),name='login'),
    path('user-detail/<int:pk>/',UserDetailUpdateDeleteAPIView.as_view(),name='user-detail'),
    
]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
 